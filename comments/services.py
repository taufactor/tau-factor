from django.db import transaction as django_db_transaction

from comments import models as comments_models
from comments import non_persistent_models as comments_non_persistent_models


class CourseCommentService(object):
    model = comments_models.CourseComment

    @classmethod
    @django_db_transaction.atomic
    def create(
            cls,
            params: comments_non_persistent_models.CreateCourseCommentParams,
    ) -> comments_models.CourseComment:
        comment = cls.model.objects.create(**{
            comments_models.CourseComment.course.field.name: params.course,
            comments_models.CourseComment.title.field.name: params.title,
            comments_models.CourseComment.content.field.name: params.content,
        })
        return comment
