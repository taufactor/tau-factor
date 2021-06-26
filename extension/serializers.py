from rest_framework import fields
from rest_framework import serializers


class GetExtensionFieldsSerializer(serializers.Serializer):
    # Find courses table
    vctb = serializers.ListField(serializers.CharField(max_length=100, read_only=True))

    # Find course table titles && relevant column positions
    vctl = fields.CharField(max_length=100, read_only=True)

    # Distinguish between course name column and course id column
    vctln = fields.CharField(max_length=100, read_only=True)
