import typing
from datetime import datetime

from django.db import transaction as django_db_transaction

from common import defines as common_defines
from teachers import defines as teachers_defines
from teachers import models as teachers_models


class TeacherService(object):
    model = teachers_models.Teacher

    @classmethod
    @django_db_transaction.atomic
    def get_or_create(
            cls,
            teacher_name: str,
            honorific: teachers_defines.Honorific,
            language: common_defines.Language,
            year: typing.Optional[int] = None,
    ) -> teachers_models.Teacher:
        year = year or datetime.today().year
        language_to_name_field = {
            common_defines.Language.EN: teachers_models.Teacher.english_teacher_name.field.name,
            common_defines.Language.HE: teachers_models.Teacher.hebrew_teacher_name.field.name,
        }

        teacher, _ = cls.model.objects.get_or_create(
            defaults={
                teachers_models.Teacher.honorific.field.name: honorific,
            },
            **{
                language_to_name_field[language]: teacher_name,
            },
        )

        if honorific > teacher.honorific:
            teacher.honorific = honorific
            teacher.save(update_fields=(teachers_models.Teacher.honorific.field.name,))

        TeacherHonorificService.get_or_create(teacher=teacher, honorific=honorific, year=year)
        return teacher


class TeacherHonorificService(object):
    model = teachers_models.Teacher

    @classmethod
    @django_db_transaction.atomic
    def get_or_create(
            cls,
            teacher: teachers_models.Teacher,
            honorific: teachers_defines.Honorific,
            year: int,
    ) -> teachers_models.Teacher:
        teacher_honorific, created = cls.model.objects.get_or_create(
            defaults={
                teachers_models.TeacherHonorific.year.field.name: year,
            },
            **{
                teachers_models.TeacherHonorific.teacher.field.name: teacher,
                teachers_models.TeacherHonorific.honorific.field.name: honorific,
            },
        )

        if not created and year > teacher_honorific.year:
            teacher_honorific.year = year
            teacher_honorific.save(
                update_fields=(
                    teachers_models.TeacherHonorific.year.field.name,
                ),
            )

        return teacher_honorific
