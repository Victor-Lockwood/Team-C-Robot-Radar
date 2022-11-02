# Referred to: https://www.geeksforgeeks.org/python-build-a-rest-api-using-flask/?id=discuss
# { DEV }	-	{ YYYY/MM/DD }	-	{ MODIFICATIONS }
# vlock     -     2022/10/30    -     Added base panoramic image functionality
# import necessary libraries and functions
import json
import os
import requests
import ast
import io

from flask import Flask, jsonify, request, send_file
from PIL import Image
from base64 import encodebytes

import data_models

# creating a Flask app
app = Flask(__name__)

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
    return send_file(pano_filepath, mimetype="image/png")


# http://localhost:5000/mapdata

# Get the current map data
# Note: Currently has dummy data
@app.route('/mapdata', methods=['GET', 'POST'])
def mapdata():
    is_test = request.args.get('istest')
    password = request.args.get("password")

    host = "localhost"
    if is_test or is_test is None:
        pass
    else:
        host = "172.17.0.2"
        port=36000

    if request.method == 'GET':
        response = Flask.response_class()
        response.content_type = "json"

        data = data_models.MapObject.get_map_objects(password)
        response.data = json.dumps(data, cls=data_models.DataModelJsonEncoder)
        return response
    else:
        map_obj1 = data_models.MapObject(1, "Can", 1, 5)
        map_obj1.create(password)

        map_obj2 = data_models.MapObject(1, "OurRobot", 8, 7)
        map_obj2.create(password)

        map_obj3 = data_models.MapObject(1, "OtherRobot", 4, 1)
        map_obj3.create(password)

        response = Flask.response_class()
        response.status_code = 201
        return response


@app.route('/logs', methods=['GET', 'POST'])
def logs():
    is_test = request.args.get('istest')
    password = request.args.get("password")

    call_port = 5432
    host = 'localhost'

    if is_test is None or ast.literal_eval(is_test):
        pass
    else:
        host = "172.17.0.2"
        call_port = 5432

    if request.method == 'GET':
        response = Flask.response_class()
        response.content_type = "json"

        data = data_models.Log.get_logs(password, call_port, host)
        response.data = json.dumps(data, cls=data_models.DataModelJsonEncoder)

        log = data_models.Log(os.path.basename(__file__), "Logs retrieved from /logs GET", log_type="Event")
        log.create(password, call_port, host)
        return response


@app.route('/autonomous', methods=['GET', 'POST'])
def autonomous():
    password = request.args.get("password")

    move_list = "r,r,r,r"
    api_url = "http://karr.local:5000/autonomous/" + move_list
    received_response = requests.get(api_url)

    return "Moved"


@app.route('/testmove', methods=['GET'])
def test_move():
    password = request.args.get("password")
    move_key = request.args.get("move_key")

    try:
        api_url = "http://karr.local:5000/right"
        response = requests.get(api_url)

        return "Test Successful"
    except Exception as ex:
        if hasattr(ex, 'message'):
            error_log = data_models.Log(os.path.basename(__file__), str(ex.message), "Error")
            error_log.create(password)
        else:
            error_log = data_models.Log(os.path.basename(__file__), str(ex), "Error")
            error_log.create(password)
        return "An error occurred - see logs"


# driver function
if __name__ == '__main__':
    # This is important for Docker
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
