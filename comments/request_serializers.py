from rest_framework import fields
from rest_framework import serializers

from comments import models as comments_models


class CourseCommentCreateSerializer(serializers.ModelSerializer):
    course_id = fields.UUIDField(required=True)
    content = fields.CharField(default="", required=False)

    class Meta:
        model = comments_models.CourseComment
        fields = (
            comments_models.CourseComment.course_id.field.attname,
            comments_models.CourseComment.title.field.name,
            comments_models.CourseComment.content.field.name,
        )
