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
    
    # Can maybe edit get_sports by letting it take a tablename argument. That way can make it more general. Can also make
    # a general 'set is_active' thing for sports, teams, and teammembers maybe

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

    def get_teams(self):
        with self._connection_manager() as connection:
            with connection.cursor(cursor_factory=extras.DictCursor) as cursor:
                cursor.execute("SELECT * FROM teams ORDER BY name;")
                rows = cursor.fetchall()
        
        return rows
    
    def add_team(self, team_name, sport_id):
        teams = self.get_teams()
        if team_name in (team['name'] for team in teams):
            return None
        
        with self._connection_manager() as connection:
            with connection.cursor() as cursor:
                sql = 'INSERT INTO teams ("name", sport_id) VALUES (%s, %s)'
                print(sql, sport_id)
                cursor.execute(sql, (team_name, (sport_id,)))
        # Unfinished here
