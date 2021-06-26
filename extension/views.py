import random

from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework import viewsets
from rest_framework import decorators as drf_decorators
from rest_framework.request import Request
from rest_framework.response import Response

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
        vctb = ["סמס", "קורס", "שם הקורס", "אופן", "קובע", "שעות", "משקל", "הערות"]
        random.shuffle(vctb)
        response_serializer = extension_serializers.GetExtensionFieldsSerializer(
            instance={
                "vctb": vctb,
                "vctl": "קורס",
                "vctln": "שם",
            },
        )
        return Response(response_serializer.data, status=status.HTTP_200_OK)
