import random

from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework import viewsets
from rest_framework import decorators as drf_decorators
from rest_framework.request import Request
from rest_framework.response import Response

from extension import defines as extension_defines
from extension import exceptions as extension_exceptions
from extension import serializers as extension_serializers

class ExtensionView(viewsets.ViewSet):
    @drf_decorators.action(
        detail=False,
        methods=["GET"],
    )
    @swagger_auto_schema(
        operation_summary="Get Collectable Fields",
        operation_description="Retrieve strings the extensions will use to capture data.",
        responses={
            status.HTTP_200_OK: extension_serializers.GetExtensionFieldsSerializer,
        },
    )
    def get_collectable_fields(self, request: Request, *args, **kwargs) -> Response:
        extension_version = request.headers.get(extension_defines.EXTENSION_VERSION_HEADER_NAME)
        if extension_version is None:
            raise extension_exceptions.NoExtensionVersionError
        if extension_version not in extension_defines.SUPPORTED_EXTENSION_VERSIONS:
            raise extension_exceptions.ExtensionDeprecatedError

        vctb = ["סמס", "קורס", "שם הקורס", "אופן", "קובע", "שעות", "משקל", "הערות"]
        random.shuffle(vctb)
        response_serializer = extension_serializers.GetExtensionFieldsSerializer(
            instance={
                "vctb": vctb[:3],
                "vctl": "קורס",
                "vctln": "שם",
            },
        )
        return Response(response_serializer.data, status=status.HTTP_200_OK)
