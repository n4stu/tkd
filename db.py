from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import current_user
from psycopg2.extras import RealDictCursor, RealDictRow
from dotmap import DotMap
from flask import g

from main import table

def convert(data):
    a = []
    if isinstance(data, RealDictRow):
        return DotMap(data)
    for item in data:
        a.append(DotMap(item))
    return a

class DB():
    def __init__(self, db):
        self.db = db
        self.cursor = db.cursor(cursor_factory=RealDictCursor)

    def update_request(self, competition_id, coach_id, sportsman_id, action):
        query = """
            BEGIN;
                CALL update_request(%s, %s, %s, %s);
            COMMIT;
        """
        self.cursor.execute(query, (competition_id, coach_id, sportsman_id, action))
        self.db.commit()

    def get_request_sportsmans(self, competition_id):
        self.cursor.execute("SELECT * FROM get_request_sportsmans(%s)", (competition_id,))
        response = self.cursor.fetchall()
        if not response:
            return False
        return convert(response)

    def get_competition_by_id(self, comp_id):
        self.cursor.execute("SELECT * FROM get_competition_by_id(%s)", (comp_id,))
        response = self.cursor.fetchone()
        if not response:
            return False
        return convert(response)

    def get_coach_sportsmans(self, coach_id):
        self.cursor.execute("SELECT * FROM get_coach_sportsmans(%s)", (coach_id,))
        response = self.cursor.fetchall()
        if not response:
            return False
        return convert(response)

    def get_clubs_cities(self):
        self.cursor.execute("SELECT * FROM get_clubs_cities()")
        response = self.cursor.fetchall()
        if not response:
            return False
        return convert(response)

    def get_filtered_clubs(self, filter):
        self.cursor.execute("SELECT * FROM get_filtered_clubs(%s)", (filter.city,))
        response = self.cursor.fetchall()
        if not response:
            return False
        return convert(response)

    def get_filtered_competitions(self, filters):
        self.cursor.execute("SELECT * FROM get_filtered_competitions(%s, %s)",
            (filters.level, filters.city))
        response = self.cursor.fetchall()
        if not response:
            return False
        return convert(response)

    def get_competitions_cities(self):
        self.cursor.execute("SELECT * FROM get_competiotions_cities()")
        response = self.cursor.fetchall()
        if not response:
            return False
        return convert(response)
    
    def get_competitions_levels(self):
        self.cursor.execute("SELECT * FROM get_competitions_levels()")
        response = self.cursor.fetchall()
        if not response:
            return False
        return convert(response)
    
    def sportsman_update_weight(self, sportsman_id, weight):
        self.cursor.execute("CALL sportsman_update_weight(%s, %s)", (sportsman_id, weight))
        self.db.commit()
    
    def get_sportsman_by_login(self, data):
        self.cursor.execute("SELECT * FROM get_sportsman_full(%s)", (data.login,))
        response = self.cursor.fetchone()
        if not response:
            return False
        return convert(response)

    def get_coach_by_login(self, data):
        self.cursor.execute("SELECT * FROM coach WHERE login=%s", (data.login,))
        response = self.cursor.fetchone()
        if not response:
            return False
        return convert(response)

    def get_user(self, user_id, table):
        if table == "sportsman":
            q = "SELECT * FROM get_sportsman_full((SELECT login FROM sportsman WHERE id = %s))"
        else:
            q = "SELECT * FROM get_coach_full((SELECT login FROM coach WHERE id = %s))"
        self.cursor.execute(q, (user_id,))
        response = self.cursor.fetchone()
        if not response:
            return False
        return convert(response)