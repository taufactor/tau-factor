from rest_framework import exceptions
from rest_framework import status


class NoExtensionVersionError(exceptions.APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "No extension version provided."
    default_code = "no_extension_version"


class ExtensionDeprecatedError(exceptions.APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Extension version is not supported anymore. Please update it."
    default_code = "extension_deprecated"
