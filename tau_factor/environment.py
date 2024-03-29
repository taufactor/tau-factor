import os
import typing
from distutils import dist


def set_env(name: str, value: str) -> None:
    os.environ[name] = value


def env_to_str(name: str, default_value: typing.Optional[str] = None) -> str:
    return os.environ[name] if default_value is None else os.getenv(name, default_value)


def env_to_bool(name: str, default_value: bool = False) -> bool:
    return dist.strtobool(os.environ.get(name, str(default_value)))


DEBUG = env_to_bool("DEBUG", True)
RUNNING_ENVIRONMENT = env_to_str("RUNNING_ENVIRONMENT", "local")

set_env("SECRET_KEY", env_to_str("SECRET_KEY", "django-insecure-)8#)_+*x9qa+!ejq@&i&t2-#t*y22$nv(k668s__7)ek^+txcd"))

# TODO: Temporary url - replace when custom domain is set
SITE_URL = env_to_str("SITE_URL", "127.0.0.1:8000")
SITE_NAME_EN = env_to_str("SITE_NAME_EN", "Tau-Factor")
SITE_NAME_HE = env_to_str("SITE_NAME_HE", "Tau פקטור")

