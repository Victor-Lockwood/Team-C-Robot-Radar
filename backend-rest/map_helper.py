import data_models
import database_handler


def update_robot(map_id, robot_position, direction,
                 password, host="localhost", port=5432, database="RobotRadarAlpha"):

    candidates = data_models.MapObject.get_map_objects(
        password=password,
        map_id=map_id,
        object_type="OurRobot",
        host=host,
        port=port,
        database=database
    )

    # We have bigger problems if we try to update a robot that doesn't exist
    our_robot = candidates[0]
    our_robot.location = robot_position
    our_robot.direction = direction
    our_robot.update_map_object_location()


def obstacle_detection(map_id, robot_position, radar_reading, direction,
                       password, host="localhost", port=5432, database="RobotRadarAlpha"):
    potential_obstacle_coordinates = \
        convert_radar_coordinates(robot_position=robot_position, radar_reading=radar_reading, direction=direction)

    p_obst_x = potential_obstacle_coordinates[0]
    p_obst_y = potential_obstacle_coordinates[1]

    map_objects = data_models.MapObject.get_map_objects(
        password=password,
        map_id=map_id,
        host=host,
        port=port,
        database=database
    )

    found_match = False

    for map_object in map_objects:
        obj_x = map_object.location[0]
        obj_y = map_object.location[1]

        if obj_x == p_obst_x and obj_y == p_obst_y:
            found_match = True
            # Got what we needed
            break

    if found_match:
        new_obstacle = data_models.MapObject(map_id=map_id, object_type="Obstacle",
                                             location_x=p_obst_x, location_y=p_obst_y)
        new_obstacle.create(password=password,host=host, port=port, database=database)

        return True
    else:
        return False



# We get our position in meters, need to convert to blocks for the map.
# Blocks are 10cm each.
def convert_robot_position(raw_robot_position, block_size=10):
    raw_robot_x = raw_robot_position[0]
    raw_robot_y = raw_robot_position[1]

    new_robot_x = round(raw_robot_x * block_size)
    new_robot_y = round(raw_robot_y * block_size)

    robot_position = (new_robot_x, new_robot_y)

    return robot_position


# Radar reading comes in cm
def __convert_radar_reading(radar_reading, block_size=10):
    return radar_reading * block_size


# robot_position needs to be converted to blocks first
def convert_radar_coordinates(direction, robot_position, radar_reading):
    radar_blocks = __convert_radar_reading(radar_reading=radar_reading)

    # This is to make sure we don't have any pass by reference funny business going on
    detected_position = robot_position + tuple()

    if direction is "W":
        detected_position = (detected_position[0] - radar_blocks, detected_position[1])
    elif direction is "E":
        detected_position = (detected_position[0] + radar_blocks, detected_position[1])
    elif direction is "N":
        detected_position = (detected_position[0], detected_position[1] + radar_blocks)
    else:
        detected_position = (detected_position[0], detected_position[1] - radar_blocks)

    return detected_position
