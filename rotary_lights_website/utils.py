import ast
from pathlib import Path
from typing import TypeVar

import environ
from django.core.exceptions import ImproperlyConfigured

T = TypeVar("T")

_DEFAULT_SECRETS_PATH = Path("/run/secrets")
_NOT_PROVIDED = "NOT PROVIDED"

env = environ.Env()


def load_secret_by_name(
    name: str,
    primitive_type: type[T] | str = str,
    *,
    default: T = _NOT_PROVIDED,
    path: str | Path = _DEFAULT_SECRETS_PATH,
) -> T:
    """Load a secret by its name.

    By default, secrets will be searched in the default docker swarm
    secrets path. To specify another location, provide `path`.

    Args:
        name (str): The name of the secret.
        primitive_type (type[T], optional): The primitive type of
        secret such as str, bool, or int. Defaults to str.
        default (T, optional): If the secret could not be found,
        return this default instead of raising `ImproperlyConfigured`.
        Defaults to _NOT_PROVIDED.
        path (str | Path, optional): The path to search for secrets.
        Defaults to _DEFAULT_SECRETS_PATH.

    Raises:
        ImproperlyConfigured: The secret could not be found and no
        default was provided.

    Returns:
        T: The value of the secret in the type indicated by
        `primitive_type` or `default` if not found.
    """
    # Convert the path parameter to a pathlib.Path.
    if isinstance(path, str):
        path = Path(path)

    try:
        filename = path / name

        # Open the file and read the secret. Then, parse it into the
        # type requested.
        with filename.open() as handle:
            data = handle.read().strip()
            if primitive_type is bool:
                return ast.literal_eval(data)
            return primitive_type(data)
    except FileNotFoundError as exc:
        if default == _NOT_PROVIDED:
            # No default was specified, so inform the caller this secret
            # could not be found.
            message = f"secret '{name}' not found"
            raise ImproperlyConfigured(message) from exc

    # Return the default as a last resort.
    return default


def load_env_variable_by_name(
    name: str,
    primitive_type: type[T] = str,
    *,
    default: T = _NOT_PROVIDED,
) -> T:
    """Load an environment variable by name.

    Args:
        name (str): The name of the environment variable to load.
        primitive_type (type[T], optional): The type of the variable
        such as str, bool, or int. Defaults to str.
        default (T | None, optional): The default value to return if the
        variable is not found. Raises `ImproperlyConfigured` if not
        provided. Defaults to _NOT_PROVIDED.

    Raises:
        ImproperlyConfigured: If the variable could not be found and no
        default was provided.

    Returns:
        T: The value of the variable, or `default` if not found.
    """
    try:
        # Search the environment variables for a variable by `name`.
        data = env.str(name)
        if primitive_type is bool:
            return ast.literal_eval(data)
        return primitive_type(data)
    except ImproperlyConfigured:
        if default == _NOT_PROVIDED:
            # No default was specified, so inform the caller this secret
            # could not be found.
            raise

    # Return the default as a last resort.
    return default


def load_setting(  # noqa: PLR0913
    name: str,
    primitive_type: type[T] = str,
    *,
    default: T = _NOT_PROVIDED,
    try_secrets: bool = True,
    try_env: bool = True,
    custom_secrets_path: str | Path = _DEFAULT_SECRETS_PATH,
) -> T:
    """
    Load a setting by a name from secrets or environment variables.

    By default, secrets will be searched in the default Docker Swarm
    secrets path. To specify another location, provide
    `custom_secrets_path`.

    Args:
        name (str): The name of the setting to load.
        primitive_type (type[T], optional): The type of the setting such
        as str, bool, or int. Defaults to str.
        default (T, optional): The default value to return if the
        setting is not found. Raises `ImproperlyConfigured` if not
        provided.
        try_secrets (bool, optional): Whether to attempt to load from
        secrets. Defaults to True.
        try_env (bool, optional): Whether to attempt to load from
        environment variables. Defaults to True.
        custom_secrets_path (str | Path, optional): The path to search
        for secrets. Defaults to _DEFAULT_SECRETS_PATH.

    Raises:
        ImproperlyConfigured: If the setting could not be found and no
        default was provided.

    Returns:
        T: The value of the setting, or `default` if not found.
    """
    last_exception = None
    if try_secrets:
        try:
            value = load_secret_by_name(
                name=name,
                primitive_type=primitive_type,
                default=default,
                path=custom_secrets_path,
            )
            if not try_env:
                return value
        except ImproperlyConfigured as e:
            last_exception = e

    if try_env:
        try:
            return load_env_variable_by_name(
                name=name,
                primitive_type=primitive_type,
                default=default,
            )
        except ImproperlyConfigured as e:
            if last_exception and default == _NOT_PROVIDED:
                raise ImproperlyConfigured(
                    f"Setting '{name}' was not found in the secrets or environment variables."
                ) from last_exception
            last_exception = e

    if default == _NOT_PROVIDED:
        if last_exception:
            raise last_exception
        raise ImproperlyConfigured(
            f"Setting '{name}' could not be found and no default value was provided."
        )

    return default
