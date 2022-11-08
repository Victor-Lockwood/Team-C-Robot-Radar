# Referred to: https://www.geeksforgeeks.org/python-build-a-rest-api-using-flask/?id=discuss
# { DEV }	-	{ YYYY/MM/DD }	-	{ MODIFICATIONS }
# vlock     -     2022/10/30    -   Added base panoramic image functionality
# vlock     -     2022/11/07    -   (Previous updates not recorded) Further cleanup and documentation
# import necessary libraries and functions
import json
import os

import requests

from flask import Flask, jsonify, request, send_file, session

import database_handler
from flask_session import Session
from PIL import Image

import data_models

# creating a Flask app
app = Flask(__name__)

# Setup session info
SESSION_TYPE = 'filesystem'
app.config.from_object(__name__)
Session(app)


# When the robot hits this, it will save the public IP to the current session.
@app.route('/initialize', methods=['GET'])
def initialize_robot_ip():
    session["robot_ip"] = request.remote_addr
    return "Got IP"


# Gets the saved public IP of the robot for the current session.
# Returns an empty string if not available.
@app.route('/checkip', methods=['GET'])
def check_ip():
    if not "robot_ip" in session:
        return ""
    else:
        return str(session["robot_ip"])


# Referred to this tutorial:
# https://www.tutorialspoint.com/python_pillow/Python_pillow_merging_images.htm
# Sends a request to the robot for pictures, then stitches the received pictures together into a panorama
# URL PARAMS:
# - istest      -   If this is a local endpoint meant to use a local Docker database (True or False).
# - password    -   Password for flaskuser.
# - remote       -   Connect to the Docker DB on Moxie (True or False).
# TODO: Handle zip file
# TODO: Implement retrieval from robot
@app.route('/panoramic', methods=['GET'])
def panoramic():
    # Get each directional image from the robot
    panel_north = Image.open('panoramic-images/north.png')
    panel_east = Image.open('panoramic-images/east.png')
    panel_south = Image.open('panoramic-images/south.png')
    panel_west = Image.open('panoramic-images/west.png')

    # We'll load these into a list so if we for some reason add more panels
    # we only have a couple places to modify
    panel_list = [panel_north, panel_east, panel_south, panel_west]

    # Defer to the first panel for dimensions
    panel_width = panel_list[0].size[0]
    panel_height = panel_list[0].size[1]

    # Resize each panel if dimensions don't match
    processed_panels = []

    for panel in panel_list:
        processed_panel = panel
        if panel.size[0] != panel_width or panel.size[1] != panel_height:
            processed_panel = panel.resize((panel_width, panel_height))
        processed_panels.append(processed_panel)

    num_panels = len(processed_panels)

    # Instantiate the panoramic image
    panoramic_image = Image.new('RGB', (num_panels * panel_width, panel_height))

    # Stitch the panels together for the full image
    for panel_position in range(num_panels):
        stitch_position = panel_position * panel_width
        panoramic_image.paste(processed_panels[panel_position], (stitch_position, 0))

    # Save the new image
    pano_filepath = "panoramic-images/full-pano.png"
    panoramic_image.save(pano_filepath)

    # Send the image home!
    response = send_file(pano_filepath, mimetype="image/png")
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


# Returns formatted map data.
# URL PARAMS (GET):
# - istest      -   If this is a local endpoint meant to use a local Docker database (True or False).
# - password    -   Password for flaskuser.
# - remote       -   Connect to the Docker DB on Moxie (True or False).
# TODO: Implement POST
@app.route('/mapdata', methods=['GET', 'POST'])
def mapdata():
    connection_info = database_handler.get_connection_info(request)

    password = connection_info[0]
    host = connection_info[1]
    call_port = connection_info[2]

    if request.method == 'GET':
        response = Flask.response_class()
        response.content_type = "json"

        data = data_models.MapObject.get_map_objects(password=password, host=host, port=call_port)
        response.data = json.dumps(data, cls=data_models.DataModelJsonEncoder)
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    else:
        map_obj1 = data_models.MapObject(map_id=1, object_type="Can", location_x=1, location_y=5)
        map_obj1.create(password=password, host=host, port=call_port)

        map_obj2 = data_models.MapObject(map_id=1, object_type="OurRobot", location_x=8, location_y=7)
        map_obj2.create(password=password, host=host, port=call_port)

        map_obj3 = data_models.MapObject(map_id=1, object_type="OtherRobot", location_x=4, location_y=1)
        map_obj3.create(password=password, host=host, port=call_port)

        response = Flask.response_class()
        response.status_code = 201
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response


# Retrieves logs from the DB.
# URL PARAMS:
# - istest      -   If this is a local endpoint meant to use a local Docker database (True or False).
# - password    -   Password for flaskuser.
# - remote       -   Connect to the Docker DB on Moxie (True or False).
@app.route('/logs', methods=['GET', 'POST'])
def logs():
    connection_info = database_handler.get_connection_info(request)

    password = connection_info[0]
    host = connection_info[1]
    call_port = connection_info[2]

    try:
        if request.method == 'GET':
            response = Flask.response_class()
            response.content_type = "json"

            data = data_models.Log.get_logs(password=password, host=host, port=call_port)
            response.data = json.dumps(data, cls=data_models.DataModelJsonEncoder)

            response.status_code = 200
            response.headers.add('Access-Control-Allow-Origin', '*')
            return response
    except Exception as ex:
        exception_message = get_exception_message(ex)

        error_log = data_models.Log(origin=os.path.basename(__file__), message=exception_message, log_type="Error")
        error_log.create(password=password, host=host, port=call_port)

        response = Flask.response_class()

        response.data = "An error occurred - see logs"
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response


# Takes formatted coordinate request and converts them to move commands for the robot.
# URL PARAMS:
# - istest      -   If this is a local endpoint meant to use a local Docker database (True or False).
# - password    -   Password for flaskuser.
# - remote       -   Connect to the Docker DB on Moxie (True or False).
@app.route('/autonomous', methods=['GET', 'POST'])
def autonomous():
    # TODO: Update this to use retrieved robot IP
    connection_info = database_handler.get_connection_info(request)

    password = connection_info[0]
    host = connection_info[1]
    call_port = connection_info[2]

    move_list = "r,r,r,r"
    api_url = "http://karr.local:5000/autonomous/" + move_list
    received_response = requests.get(api_url)

    return "Moved"


# Takes a move character and sends the corresponding move command to the robot.
# URL PARAMS:
# - istest      -   If this is a local endpoint meant to use a local Docker database (True or False).
# - password    -   Password for flaskuser.
# - remote       -   Connect to the Docker DB on Moxie (True or False).
# - movekey     -   The movement keyboard key hit (W, A, S or D).
@app.route('/move', methods=['GET'])
def move():
    connection_info = database_handler.get_connection_info(request)

    password = connection_info[0]
    host = connection_info[1]
    call_port = connection_info[2]

    move_key = request.args.get("movekey")

    response = Flask.response_class()
    try:
        match move_key:
            case "W":
                api_url = "<ENTER IP HERE>/forward"
                response = requests.get(api_url)
            case "S":
                api_url = "<ENTER IP HERE>/backward"
                response = requests.get(api_url)
            case "A":
                api_url = "<ENTER IP HERE>/left"
                response = requests.get(api_url)
            case "D":
                api_url = "<ENTER IP HERE>/right"
                response = requests.get(api_url)

        return response
    except Exception as ex:
        exception_message = get_exception_message(ex)

        error_log = data_models.Log(origin=os.path.basename(__file__), message=exception_message, log_type="Error")
        error_log.create(password=password, host=host, port=call_port)

        return "An error occurred - see logs"


# Test moving the robot over the Interwebs.
# No URL params
@app.route('/testrobotconnect', methods=['GET'])
def test_robot_connect():
    try:
        api_url = "<ENTER IP HERE>/right"
        response = requests.get(api_url)

        return "Test connect to robot successful!"
    except Exception as ex:
        return "Could not reach robot."


def get_exception_message(ex):
    if hasattr(ex, 'message'):
        return str(ex.message)
    else:
        return str(ex)


# driver function
if __name__ == '__main__':
    # This is important for Docker
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
