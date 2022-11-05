# Referred to: https://www.geeksforgeeks.org/python-build-a-rest-api-using-flask/?id=discuss
# { DEV }	-	{ YYYY/MM/DD }	-	{ MODIFICATIONS }
# vlock     -     2022/10/30    -     Added base panoramic image functionality
# import necessary libraries and functions
import json
import os
import string

import requests
import ast
import io

from flask import Flask, jsonify, request, send_file, session

import database_handler
from flask_session import Session
from PIL import Image

import data_models

# creating a Flask app
app = Flask(__name__)
SESSION_TYPE = 'filesystem'
app.config.from_object(__name__)
Session(app)


@app.route('/initialize', methods=['GET'])
def initialize_robot_ip():
    session["robot_ip"] = request.remote_addr
    return "Got IP"


@app.route('/checkip', methods=['GET'])
def check_ip():
    if not "robot_ip" in session:
        return ""
    else:
        return str(session["robot_ip"])


@app.route('/camera', methods=['GET'])
def camera():
    api_url = "http://karr.local:5000/camera"

    response = requests.post(api_url)
    memory_image = io.BytesIO(response.content)
    panoramic_image = Image.open(memory_image)
    panoramic_image.show()

    return "Success"


# Referred to this tutorial:
# https://www.tutorialspoint.com/python_pillow/Python_pillow_merging_images.htm
@app.route('/panoramic', methods=['GET'])
def panoramic():
    # Get each directional image from the robot
    # TODO: Need to get these images from the robot
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


# http://localhost:5000/mapdata

# Get the current map data
# Note: Currently has dummy data
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
        return response


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

            log = data_models.Log(origin=os.path.basename(__file__), message="Logs retrieved from /logs GET", log_type="Event")
            log.create(password=password, port=call_port, host=host)
            return response
    except Exception as ex:
        exception_message = get_exception_message(ex)

        error_log = data_models.Log(origin=os.path.basename(__file__), message=exception_message, log_type="Error")
        error_log.create(password=password, host=host, port=call_port)

        return "An error occurred - see logs"


@app.route('/autonomous', methods=['GET', 'POST'])
def autonomous():
    # TODO: Update this to use retrieved robot IP
    password = request.args.get("password")

    move_list = "r,r,r,r"
    api_url = "http://karr.local:5000/autonomous/" + move_list
    received_response = requests.get(api_url)

    return "Moved"


@app.route('/testmove', methods=['GET'])
def test_move():
    connection_info = database_handler.get_connection_info(request)

    password = connection_info[0]
    host = connection_info[1]
    call_port = connection_info[2]

    move_key = request.args.get("move_key")

    try:
        api_url = "http://karr.local:5000/right"
        response = requests.get(api_url)

        return "Test Successful"
    except Exception as ex:
        exception_message = get_exception_message(ex)

        error_log = data_models.Log(origin=os.path.basename(__file__), message=exception_message, log_type="Error")
        error_log.create(password=password, host=host, port=call_port)

        return "An error occurred - see logs"


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
