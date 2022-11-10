import data_models
import database_handler


def obstacle_detection(robot_position, radar_reading,
                       password, host="localhost", port=5432, database="RobotRadarAlpha"):
    conn = database_handler.get_connection(password, host, database, port)
    cur = conn.cursor()

    cur.execute('SELECT * FROM "MapObject"')
    rows = cur.fetchall()

    map_objects = list()



    print('bleeehhhh')