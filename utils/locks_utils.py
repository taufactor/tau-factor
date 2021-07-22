from contextlib import contextmanager

from django.db import connection as db_connection
from django_pglocks import advisory_lock as pglocks


@contextmanager
def advisory_lock(*args, **kwargs):
    if db_connection.vendor == "postgresql":
        with pglocks(*args, **kwargs) as lock:
            yield lock
    else:
        yield
