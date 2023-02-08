import os
import re
import uuid

base_name = "ratings_courserating"
in_filename = os.path.join("..", "db", F"{base_name}.sql")
out_filename = os.path.join("..", "db", F"{base_name}.bulk.sql")
bulk_size = 10000


def add_bulk_insert(f, prefix, values):
    values_str = ',\n'.join(values)
    f.write(F"{prefix}{values_str};\n")


def split_values(values_line):
    p = re.compile(r"\((.*),replace\((.*),.*,char\(10\)\),(.*)\)")
    results = p.search(values_line)
    if results is None:
        return [values_line]

    pk = results.group(1)
    names = set(results.group(2).strip("'").split("\\n"))
    course_group_id = results.group(3)

    rows = [F"({pk},'{names[0]}',{course_group_id})"]
    for name in names[1:]:
        rows.append(F"('{str(uuid.uuid4()).replace('-','')}','{name}',{course_group_id})")

    return rows


with open(out_filename, "w", encoding="utf8") as out_file:
    bulk_values = []
    insert_prefix = None
    with open(in_filename, "r", encoding="utf8") as in_file:
        pattern = re.compile(r"(.*VALUES)(\(.*\));\n")
        for line in in_file.readlines():
            result = pattern.search(line)
            
            if insert_prefix is None:
                insert_prefix = result.group(1)

            bulk_values.append(result.group(2))
            #values = split_values(result.group(2))
            #bulk_values.extend(values)

            if len(bulk_values) >= bulk_size:
                add_bulk_insert(out_file, insert_prefix, bulk_values)
                bulk_values = []

        if len(bulk_values) > 0:
            add_bulk_insert(out_file, insert_prefix, bulk_values)
