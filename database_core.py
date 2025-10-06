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
                cursor.execute("SELECT * FROM sports ORDER BY name;")
                rows = cursor.fetchall()
        
        return rows
    
    def add_sports(self, potentional_id):
        sport_lst = self.get_sports()
        valid_ids = {row['id'] for row in sport_lst}
        
        try:
            potentional_id = int(potentional_id)
        except ValueError:
            return None

        if potentional_id in valid_ids:
            with self._connection_manager() as connection:
                with connection.cursor() as cursor:
                    sql = "UPDATE sports SET is_active = true WHERE id = %s;"
                    potentional_id = str(potentional_id)
                    cursor.execute(sql, (potentional_id,))

    def remove_sport(self, sport_id):
        sport_lst = self.get_sports()
        valid_ids = {row['id'] for row in sport_lst}
        
        try:
            sport_id = int(sport_id)
        except ValueError:
            return None

        if sport_id in valid_ids:
            with self._connection_manager() as connection:
                with connection.cursor() as cursor:
                    sql = "UPDATE sports SET is_active = false WHERE id = %s;"
                    sport_id = str(sport_id)
                    cursor.execute(sql, (sport_id,))