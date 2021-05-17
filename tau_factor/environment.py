import os
from distutils import dist


def env_to_str(name: str, default_value: str = None) -> str:
    return os.environ.get(name, default_value)


def env_to_bool(name: str, default_value: bool = False) -> bool:
    return dist.strtobool(os.environ.get(name, str(default_value)))


DEBUG = env_to_bool("DEBUG", False)

SITE_URL = env_to_str("SITE_URL", "www.tau-factor.com")
SITE_NAME_EN = env_to_str("SITE_NAME_EN", "Tau-Factor")
SITE_NAME_HE = env_to_str("SITE_NAME_HE", "Tau פקטור")
