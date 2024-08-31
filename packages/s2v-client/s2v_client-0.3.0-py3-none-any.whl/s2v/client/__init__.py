import abc
import datetime
import enum
import io
import os
import pathlib
import shutil
import tempfile
import typing
import zipfile
from collections.abc import Callable
from contextlib import AbstractContextManager
from types import TracebackType
from typing import IO, Any, Literal

import click
import google.auth
import httpx
import msal.token_cache
import platformdirs
from google.auth import credentials, exceptions, external_account, impersonated_credentials
from google.auth.transport import requests

from s2v.client.auth import AzureCredentials, FileTokenCache
from s2v.version import version


def _google_auth(
    source_credentials: credentials.Credentials, audience: str
) -> Callable[[httpx.Request], httpx.Request]:
    if isinstance(source_credentials, external_account.Credentials):
        # External account credentials are not supported in the IDTokenCredentials directly yet.
        # See https://github.com/googleapis/google-auth-library-python/issues/1252
        source_credentials = source_credentials._initialize_impersonated_credentials()  # noqa: SLF001

    id_token_credentials = impersonated_credentials.IDTokenCredentials(source_credentials, audience, include_email=True)
    transport = requests.Request()

    def authenticate(request: httpx.Request) -> httpx.Request:
        id_token_credentials.before_request(transport, request.method, request.url, request.headers)
        return request

    return authenticate


def _zip_directory_contents(dir: pathlib.PurePath, target: IO[bytes]) -> None:
    """
    Creates a ZIP archive of the given directory's contents, recursively.

    :param dir: the directory to search for contents to be zipped
    :param target: a target IO to write the ZIP archive to
    """

    with zipfile.ZipFile(target, "w", compression=zipfile.ZIP_LZMA) as zip_file:
        for directory_name, _, files in os.walk(dir):
            directory = pathlib.PurePath(directory_name)
            zip_file.write(directory, directory.relative_to(dir))
            for file_name in files:
                file = directory / file_name
                zip_file.write(file, file.relative_to(dir))


class AuthMode(str, enum.Enum):
    NONE = "none"
    AUTO = "auto"
    USER = "user"


class S2VConfig(AbstractContextManager["S2VConfig"]):
    def __init__(self, config_dir: pathlib.Path):
        self.config_dir = config_dir
        self.token_cache = FileTokenCache(config_dir / "token_cache.json")
        self.credentials_config_path = config_dir / "credentials.json"

    def __enter__(self) -> "S2VConfig":
        self.token_cache.__enter__()
        return self

    def __exit__(
        self, exc_type: type[BaseException] | None, exc_val: BaseException | None, exc_tb: TracebackType | None
    ) -> Literal[False]:
        return self.token_cache.__exit__(exc_type, exc_val, exc_tb)


class S2VError(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message

    def __str__(self) -> str:
        return self.message


def setup_credentials(
    auth_mode: AuthMode,
    token_cache: msal.token_cache.TokenCache | None = None,
    credentials_config_path: pathlib.Path | None = None,
) -> credentials.Credentials | None:
    match auth_mode:
        case AuthMode.AUTO:
            if credentials_config_path and credentials_config_path.exists():
                return AzureCredentials.from_file(credentials_config_path, token_cache=token_cache)
            adc, _ = google.auth.default()
            return typing.cast(credentials.Credentials, adc)
        case AuthMode.USER:
            if credentials_config_path is None:
                msg = "credentials_config_path is a mandatory parameter for user auth"
                raise ValueError(msg)
            if not credentials_config_path.exists():
                msg = "Please log in first."
                raise S2VError(msg)
            return AzureCredentials.from_file(credentials_config_path, token_cache=token_cache)
        case _:
            return None


class ValidationResult(abc.ABC):
    @abc.abstractmethod
    def __bool__(self) -> bool: ...


class ValidationSuccess(ValidationResult):
    def __bool__(self) -> Literal[True]:
        return True

    def __str__(self) -> str:
        return "OK"


class ValidationFailure(ValidationResult):
    def __init__(self, details: list[str]) -> None:
        self.details = details

    def __bool__(self) -> Literal[False]:
        return False

    def __str__(self) -> str:
        return "\n".join(self.details)


class S2VClient:
    def __init__(self, client: httpx.Client):
        self._httpx_client = client

    @classmethod
    def create(cls, base_url: str | httpx.URL, creds: credentials.Credentials | None) -> "S2VClient":
        authorization = _google_auth(creds, str(base_url)) if creds else None
        headers = {"User-Agent": f"s2v-client/{version}"}
        timeout = httpx.Timeout(timeout=datetime.timedelta(minutes=1).total_seconds())
        return cls(httpx.Client(base_url=base_url, auth=authorization, headers=headers, timeout=timeout))

    def validate(self, input_dir: pathlib.PurePath) -> ValidationResult:
        with tempfile.TemporaryFile(suffix=".zip") as zip_file:
            _zip_directory_contents(input_dir, zip_file)
            zip_file.seek(0)

            response = self._httpx_client.post(
                "/v1/validate",
                content=zip_file,
                headers={"Accept": "text/plain", "Accept-Encoding": "gzip", "Content-Type": "application/zip"},
            )

        match response.status_code:
            case httpx.codes.OK:
                return ValidationSuccess()
            case httpx.codes.UNPROCESSABLE_ENTITY:
                return ValidationFailure(response.text.splitlines())
            case _:
                response.raise_for_status()
                # This is unreachable, because raise_for_status() will already raise an error.
                # However, we need to convince the type checker that no return statement is missing.
                raise  # noqa: PLE0704

    def generate(self, input_dir: pathlib.PurePath, output_dir: pathlib.PurePath) -> None:
        with tempfile.TemporaryFile(suffix=".zip") as request_data:
            _zip_directory_contents(input_dir, request_data)
            request_data.seek(0)

            response = self._httpx_client.post(
                "/v1/generate",
                content=request_data,
                headers={"Accept": "application/zip", "Content-Type": "application/zip"},
            )

            match response.status_code:
                case httpx.codes.UNPROCESSABLE_ENTITY:
                    raise S2VError(response.text)
                case _:
                    response.raise_for_status()

        with zipfile.ZipFile(io.BytesIO(response.content), "r") as response_zip:
            response_zip.extractall(output_dir)


class _URLParamType(click.ParamType):
    name = "URL"

    def convert(self, value: Any, param: click.Parameter | None, ctx: click.Context | None) -> httpx.URL:
        try:
            return httpx.URL(value)
        except (TypeError, httpx.InvalidURL) as err:
            self.fail(f"{value!r} is not a valid {self.name}: {err}", param, ctx)


@click.group(name="s2v", help=f"Stream2Vault CLI {version}")
@click.option(
    "--config-dir",
    help="Path to user configuration directory",
    type=click.Path(file_okay=False, path_type=pathlib.Path),
    default=platformdirs.user_config_path("s2v-client"),
    show_default=True,
)
@click.pass_context
def cli(ctx: click.Context, config_dir: pathlib.Path) -> None:
    ctx.obj = ctx.with_resource(S2VConfig(config_dir))


input_dir_opt = click.option(
    "-i",
    "--input",
    type=click.Path(exists=True, file_okay=False, path_type=pathlib.PurePath),
    required=True,
    help="Path to the input directory",
)
output_dir_opt = click.option(
    "-o",
    "--output",
    type=click.Path(file_okay=False, writable=True, path_type=pathlib.PurePath),
    required=True,
    help="Path to the output directory",
)
url_opt = click.option(
    "-u",
    "--url",
    type=_URLParamType(),
    required=True,
    help="URL of the S2V server to connect to",
)
auth_mode_opt = click.option(
    "--auth-mode",
    type=click.Choice(list(AuthMode), case_sensitive=False),
    default=AuthMode.AUTO,
    show_default=True,
    help="How to authenticate to the server",
)


@cli.command("validate", help="Validate vault model")
@input_dir_opt
@url_opt
@auth_mode_opt
@click.pass_obj
@click.pass_context
def validate(
    ctx: click.Context, s2v_config: S2VConfig, input: pathlib.PurePath, url: httpx.URL, auth_mode: AuthMode
) -> None:
    try:
        creds = setup_credentials(auth_mode, s2v_config.token_cache, s2v_config.credentials_config_path)
        client = S2VClient.create(url, creds)
        result = client.validate(input)
        if isinstance(result, ValidationFailure):
            print(result)
            ctx.exit(1)
    except BaseException as err:
        raise click.ClickException(str(err)) from err


@cli.command("generate", help="Generate deployment artifacts for vault model")
@input_dir_opt
@output_dir_opt
@url_opt
@auth_mode_opt
@click.pass_obj
def generate(
    s2v_config: S2VConfig, input: pathlib.PurePath, output: pathlib.PurePath, url: httpx.URL, auth_mode: AuthMode
) -> None:
    try:
        creds = setup_credentials(auth_mode, s2v_config.token_cache, s2v_config.credentials_config_path)
        client = S2VClient.create(url, creds)
        client.generate(input, output)
    except BaseException as err:
        raise click.ClickException(str(err)) from err


@cli.command("login", help="Authorize the S2V CLI to access the S2V service")
@click.option(
    "-c",
    "--config",
    type=click.Path(dir_okay=False, path_type=pathlib.Path),
    required=True,
    help="Path to your auth config file",
)
@click.pass_obj
def login(s2v_config: S2VConfig, config: pathlib.Path) -> None:
    try:
        azure_creds = AzureCredentials.from_file(config, token_cache=s2v_config.token_cache)
        azure_creds.login()
    except exceptions.GoogleAuthError as err:
        raise click.ClickException(str(err)) from err
    s2v_config.config_dir.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(config, s2v_config.credentials_config_path)
    print("Login successful.")


def main() -> None:
    terminal_size = shutil.get_terminal_size()
    cli(auto_envvar_prefix="S2V", max_content_width=terminal_size.columns)
