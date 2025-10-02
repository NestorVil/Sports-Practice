import psycopg2
from psycopg2 import extras
from contextlib import contextmanager


class DatabaseCore():
    @contextmanager
    def _connection_manager(self):
        connection = psycopg2.connect(dbname='sports')
        try:
            with connection:
                yield connection
        finally:
            connection.close()


    def get_sports(self):
        with self._connection_manager() as connection:
            with connection.cursor(cursor_factory=extras.DictCursor) as cursor:
                cursor.execute("SELECT name FROM sports;")
                rows = cursor.fetchall()
        
        return [row['name'] for row in rows]
