from rest_framework import serializers

from comments import models as comments_models


class CourseCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = comments_models.CourseComment
        fields = (
            comments_models.CourseComment.comment_id.field.attname,
            comments_models.CourseComment.course_id.field.attname,
            comments_models.CourseComment.title.field.name,
            comments_models.CourseComment.content.field.name,
            comments_models.CourseComment.post_date.field.name,
            comments_models.CourseComment.parent_comment_id.field.attname,
        )
