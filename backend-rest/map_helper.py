import data_models
import database_handler


def obstacle_detection(map_id, robot_position, radar_reading,
                       password, host="localhost", port=5432, database="RobotRadarAlpha"):

    map_objects = data_models.MapObject.get_map_objects(
                    password=password,
                    map_id=map_id,
                    host=host,
                    port=port,
                    database=database
                )


