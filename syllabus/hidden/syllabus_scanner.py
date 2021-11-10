import logging

from syllabus import syllabus_consumer
from syllabus import syllabus_loader


def scan(year: int) -> None:
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s: %(message)s',
    )

    loader = syllabus_loader.SyllabusLoader(year=year)
    consumer = syllabus_consumer.SyllabusConsumer()
    loader.set_consumer(consumer.consumer)
    loader.run()

    with open("courses.txt", "w", encoding="utf8") as f:
        for course_info in consumer.courses:
            f.write(F"Course code {course_info.course_code}:\n")
            for course_group_info in course_info.course_groups:
                f.write(F"\tGroup {course_group_info.course_group_name}\n")
                f.write(F"\t\tCourse name {course_group_info.course_name}\n")
                f.write(F"\t\tSemester {course_group_info.semester.value}\n")
                f.write(F"\t\tFaculty {course_group_info.faculty}\n")
                f.write(F"\t\tSchool {course_group_info.school}\n")
                f.write("\t\tMeetings:\n")
                for meeting in course_group_info.meetings:
                    teachers = ", ".join(str(teacher) for teacher in meeting.teachers)
                    f.write(F"\t\t\t{meeting.starting_time}-{meeting.ending_time} - {teachers}\n")
