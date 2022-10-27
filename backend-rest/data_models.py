from json import JSONEncoder
from datetime import date, datetime
import psycopg2

import database_handler


class Map:
    def __init__(self):
        print("placeholder")


class Log:
    def __init__(self, origin, message, log_type, stack_trace="", created_at=None, id=None):
        self.created_at = created_at
        self.origin = origin
        self.message = message
        self.log_type = log_type
        self.stack_trace = stack_trace
        self.id = id

    def create(self, password, host="localhost", database="RobotRadarAlpha"):
        conn = database_handler.get_connection(password, host, database)
        cur = conn.cursor()

        cur.execute('INSERT INTO "Logs" ("Origin", "Message", "Type", "StackTrace")'
                    'VALUES (%s, %s, %s, %s)',
                    (self.origin,
                     self.message,
                     self.log_type,
                     self.stack_trace))

        conn.commit()

        cur.close()
        conn.close()

        print("Successfully inserted a log!")

    @staticmethod
    def get_logs(password, host="localhost", database="RobotRadarAlpha"):
        conn = database_handler.get_connection(password, host, database)
        cur = conn.cursor()

        cur.execute('SELECT * FROM "Logs"')
        rows = cur.fetchall()

        logs = list()

        for row in rows:
            id = row[0]
            created_at = row[1]
            origin = row[2]
            message = row[3]
            log_type = row[4]
            stacktrace = row[5]

            log_record = Log(origin, message, log_type, stacktrace, created_at, id)
            logs.append(log_record)

        return logs


class MapObject:
    def __init__(self, map_id, object_type, location_x, location_y, direction=None, created_at=None, id=None):
        self.map_id = map_id
        self.object_type = object_type
        self.location = (location_x, location_y)
        self.created_at = created_at
        self.direction = direction
        self.id = id

    def create(self, password, host="localhost", database="RobotRadarAlpha"):
        conn = database_handler.get_connection(password, host, database)
        cur = conn.cursor()

        cur.execute('INSERT INTO "MapObject" ("MapId", "ObjectType", "Direction", "LocationX", "LocationY")'
                    'VALUES (%s, %s, %s, %s, %s)',
                    (self.map_id,
                     self.object_type,
                     self.direction,
                     self.location[0],
                     self.location[1]))

        conn.commit()

        cur.close()
        conn.close()

        print("Successfully inserted a map object!")

    @staticmethod
    def get_map_objects(password, host="localhost", database="RobotRadarAlpha"):
        conn = database_handler.get_connection(password, host, database)
        cur = conn.cursor()

        cur.execute('SELECT * FROM "MapObject"')
        rows = cur.fetchall()

        map_objects = list()

        for row in rows:
            id = row[0]
            created_at = row[1]
            map_id = row[2]
            object_type = row[3]
            direction = row[4]
            location_x = row[5]
            location_y = row[6]

            map_object_record = MapObject(map_id, object_type, location_x, location_y, direction, created_at, id)
            map_objects.append(map_object_record)

        return map_objects


class DataModelJsonEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, (datetime, date)):
            return o.isoformat()
        return o.__dict__


def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError("Type %s not serializable" % type(obj))
