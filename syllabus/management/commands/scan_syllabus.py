import typing
from datetime import datetime

from django.core.management import base as django_management_base
from syllabus_scanner import non_persistent_models as syllabus_scanner_non_persistent_models
from syllabus_scanner import scanner


class Command(django_management_base.BaseCommand):
    help = 'Scan syllabus site for new courses'

    @staticmethod
    def _get_language(language_name: str) -> syllabus_scanner_non_persistent_models.Language:
        return getattr(syllabus_scanner_non_persistent_models.Language, language_name)

    @staticmethod
    def _get_departments(
            department_names: typing.Optional[typing.Sequence[str]],
    ) -> typing.Sequence[syllabus_scanner_non_persistent_models.Department]:
        if department_names is None:
            return tuple()
        return tuple(
            getattr(syllabus_scanner_non_persistent_models.Department, department_name)
            for department_name in sorted(set(department_names))
        )

    @staticmethod
    def _get_default_year() -> int:
        today = datetime.today()
        # Move to next year on August.
        # Notice that a academic year is always the one that is starts at.
        # So between January-July we still need to take the previous year.
        # After that, we move to the next school year.
        default_year = today.year if today.month >= 8 else today.year - 1
        return default_year

    def add_arguments(self, parser: django_management_base.CommandParser) -> None:
        parser.add_argument(
            "--lang",
            choices=tuple(language.name for language in syllabus_scanner_non_persistent_models.Language.all()),
            default=syllabus_scanner_non_persistent_models.Language.hebrew.name,
            help="The syllabus language to load",
        )
        parser.add_argument(
            "--year",
            default=self._get_default_year(),
            type=int,
            help="The Gregorian year the school year starts at",
        )
        parser.add_argument(
            "--department",
            choices=tuple(department.name for department in syllabus_scanner_non_persistent_models.Department.all()),
            nargs="+",
            help="The department name(s) to scan",
        )

    def handle(self, *args, **options) -> None:
        import time
        start = time.time()
        results = scanner.scan(
            language=self._get_language(options["lang"]),
            year=options["year"],
            departments=self._get_departments(options["department"]),
        )
        end = time.time()
        print(end-start)
        print(F"Courses count={len(results.courses)}")
        print(F"Failure count={len(results.failures)}")
        # print(results.serialize_text())
