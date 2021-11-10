import re

URL = "https://www.ims.tau.ac.il/tal/kr/Search_L.aspx"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"
HEADERS = {"User-Agent": USER_AGENT}

DEPS_TO_LOAD = (
    "08",
    "05",
    "10",
    "04",
    "06-16",
    "03-09",
    "14",
    "12",
    "01",
    "11-07-15",
    "2171-2172",
    "1880-1882-1883",
    "1843",
    "2120",
)

PAGE_QUEUE_SIZE = len(DEPS_TO_LOAD) * 2

YEAR_PATTERN = re.compile(r"^.*\((\d{4})/\d{4}\)$")
COURSE_AND_GROUP_PATTERN = re.compile(r"^(\d{4}-\d{4})\s+קב':\s(\d{2})$")
FACULTY_AND_SCHOOL_PATTERN = re.compile(r"^(.*)/(.*)$")
