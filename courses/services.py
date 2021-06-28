from django.db import models as django_db_models
from django.db import transaction as django_db_transaction

from courses import defines as courses_defines
from courses import models as courses_models
from courses import non_persistent_models as courses_non_persistent_models
from ratings import services as ratings_services


class CourseService(object):
    model = courses_models.Course

    @classmethod
    @django_db_transaction.atomic
    def get_or_create(
            cls,
            course_code: str,
    ) -> courses_models.Course:
        course, _ = cls.model.objects.get_or_create(
            defaults={},
            **{
                courses_models.Course.course_code.field.name: course_code,
            },
        )
        ratings_services.CourseRatingService.get_or_create(course=course)
        return course

    @classmethod
    def update_most_common_names(cls, course: courses_models.Course) -> None:
        count_annotation = "repetitions"

        new_most_common_names = []

        for language in courses_defines.Language:
            most_common_course_name_qs = courses_models.CourseInstanceName.objects.filter(**{
                "__".join((
                    courses_models.CourseInstanceName.course_instance.field.name,
                    courses_models.CourseInstance.course.field.name,
                )): course,
                courses_models.CourseInstanceName.language.field.name: language,
            }).values(
                courses_models.CourseInstanceName.course_name.field.name,
            ).annotate(**{
                count_annotation: django_db_models.Count("*"),
            }).order_by(
                f"-{count_annotation}",
            )[:1]
            if len(most_common_course_name_qs) > 0:
                most_common_course_name = most_common_course_name_qs[0]
                new_most_common_names.append(
                    courses_models.CourseCommonName(**{
                        courses_models.CourseCommonName.course.field.name: course,
                        courses_models.CourseCommonName.language.field.name: language,
                        courses_models.CourseCommonName.course_name.field.name:
                            most_common_course_name[courses_models.CourseCommonName.course_name.field.name],
                    }),
                )

        with django_db_transaction.atomic():
            course.most_common_names.all().delete()
            for new_most_common_name in new_most_common_names:
                new_most_common_name.save()


class CourseInstanceService(object):
    model = courses_models.CourseInstance

    @classmethod
    @django_db_transaction.atomic
    def get_or_create(
            cls,
            params: courses_non_persistent_models.CreateCourseInstanceParams,
    ) -> courses_models.CourseInstance:
        course = CourseService.get_or_create(course_code=params.course_code)

        course_instance, created = cls.model.objects.get_or_create(
            defaults={},
            **{
                courses_models.CourseInstance.course.field.name: course,
                courses_models.CourseInstance.year.field.name: params.year,
                courses_models.CourseInstance.semester.field.name: params.semester,
            },
        )

        if created is True:
            # If the course instance is actually created, then we do not pass through
            # the manager's get_queryset, and annotations are not added.
            # We can be sure that there are no groups currently connected to this course instance.
            course_instance.num_groups = 0

        course_instance_names = tuple(
            courses_models.CourseInstanceName(**{
                courses_models.CourseInstanceName.course_instance.field.name: course_instance,
                courses_models.CourseInstanceName.language.field.name: language,
                courses_models.CourseInstanceName.course_name.field.name: course_name,
            })
            for language, course_name in params.course_instance_names.items()
        )
        courses_models.CourseInstanceName.objects.bulk_create(course_instance_names, ignore_conflicts=True)
        CourseService.update_most_common_names(course)

        return course_instance


class CourseGroupService(object):
    model = courses_models.CourseGroup

    @classmethod
    @django_db_transaction.atomic
    def get_or_create(
            cls,
            params: courses_non_persistent_models.CreateCourseGroupParams,
    ) -> courses_models.CourseGroup:
        course_group, created = cls.model.objects.get_or_create(
            defaults={},
            **{
                courses_models.CourseGroup.course_instance.field.name: params.course_instance,
                courses_models.CourseGroup.course_group_name.field.name: params.group_name,
            },
        )

        if created is True:
            # If the course group is actually created, then we do not pass through
            # the manager's get_queryset, and annotations are not added.
            # We can be sure that there are no exams currently connected to this course group.
            course_group.num_exams = 0

        course_group_teachers = tuple(
            courses_models.CourseGroupTeacher(**{
                courses_models.CourseGroupTeacher.course_group.field.name: course_group,
                courses_models.CourseGroupTeacher.teacher_name.field.name: teacher_name,
            })
            for teacher_name in params.teacher_names
        )
        courses_models.CourseGroupTeacher.objects.bulk_create(course_group_teachers, ignore_conflicts=True)

        return course_group
