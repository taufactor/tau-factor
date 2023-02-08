import uuid

from enumchoicefield import EnumChoiceField
from django.core import validators as django_validators
from django.db import models as django_db_models

from common import defines as commons_defines
from teachers import defines as teachers_defines


class Teacher(django_db_models.Model):
    TEACHER_HONORIFICS = "honorifics"

    teacher_id = django_db_models.UUIDField(primary_key=True, default=uuid.uuid4)

    hebrew_first_name = django_db_models.CharField(
        max_length=teachers_defines.TEACHER_NAME_MAX_LENGTH,
        null=False,
        db_index=True,
    )

    hebrew_last_name = django_db_models.CharField(
        max_length=teachers_defines.TEACHER_NAME_MAX_LENGTH,
        null=False,
        db_index=True,
    )

    english_first_name = django_db_models.CharField(
        max_length=teachers_defines.TEACHER_NAME_MAX_LENGTH,
        null=False,
        db_index=True,
    )

    english_last_name = django_db_models.CharField(
        max_length=teachers_defines.TEACHER_NAME_MAX_LENGTH,
        null=False,
        db_index=True,
    )

    honorific = EnumChoiceField(teachers_defines.Honorific, null=False)

    email = django_db_models.EmailField(null=False, unique=True)

    class Meta:
        indexes = (
            django_db_models.Index(fields=("hebrew_first_name", "hebrew_last_name",)),
            django_db_models.Index(fields=("english_first_name", "english_last_name")),
        )

    @property
    def full_name(self) -> str:
        return f"{self.english_first_name} {self.english_last_name}"

    @property
    def hebrew_honorific(self) -> str:
        return self.honorific.to_string(language=commons_defines.Language.HE)

    @property
    def english_honorific(self) -> str:
        return self.honorific.to_string(language=commons_defines.Language.EN)

    def __repr__(self):
        return f"{self.english_honorific} {self.full_name}"

    def __str__(self):
        return f"Teacher({repr(self)})"


class TeacherHonorific(django_db_models.Model):
    teacher_honorific_id = django_db_models.UUIDField(primary_key=True, default=uuid.uuid4)

    teacher = django_db_models.ForeignKey(
        Teacher,
        on_delete=django_db_models.CASCADE,
        related_name=Teacher.TEACHER_HONORIFICS,
    )
    honorific = EnumChoiceField(teachers_defines.Honorific, null=False)

    year = django_db_models.PositiveIntegerField(
        null=False,
        validators=(
            django_validators.MinValueValidator(2000),
            django_validators.MaxValueValidator(2040),
        ),
    )

    class Meta:
        unique_together = ("teacher", "honorific")

    def __repr__(self):
        return self.honorific.to_string(language=commons_defines.Language.EN)

    def __str__(self):
        return f"TeacherHonorific({repr(self)})"
