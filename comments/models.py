import uuid

from django.db import models as django_db_models

from courses import models as courses_models


class CourseCommentManager(django_db_models.Manager):
    def get_queryset(self):
        return super(CourseCommentManager, self).get_queryset().filter(**{
            CourseComment.hidden.field.name: False,
        })


class CourseComment(django_db_models.Model):
    CHILD_COMMENTS_FIELD_NAME = "child_comments"

    comment_id = django_db_models.UUIDField(primary_key=True, default=uuid.uuid4)

    course = django_db_models.ForeignKey(
        courses_models.Course,
        on_delete=django_db_models.CASCADE,
        related_name=courses_models.Course.COURSE_COMMENTS_FIELD_NAME,
    )

    title = django_db_models.CharField(max_length=255, null=False)
    content = django_db_models.TextField(null=False)
    post_date = django_db_models.DateTimeField(auto_now_add=True, blank=True)

    parent_comment = django_db_models.ForeignKey(
        "self",
        blank=True,
        null=True,
        on_delete=django_db_models.CASCADE,
        related_name=CHILD_COMMENTS_FIELD_NAME,
    )

    hidden = django_db_models.BooleanField(blank=True, default=False)

    # If we start supporting logins, then we connect a comment to a user

    class Meta:
        ordering = ("course", "post_date",)

    objects = CourseCommentManager()
    all_objects = django_db_models.Manager()

    def __repr__(self):
        suffix = " (hidden)" if self.hidden else ""
        return f"{repr(self.course)}, Title '{self.title}', Posted at {self.post_date}{suffix}"

    def __str__(self):
        return f"CourseComment({repr(self)})"
