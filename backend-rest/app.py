# Referred to: https://www.geeksforgeeks.org/python-build-a-rest-api-using-flask/?id=discuss
# { DEV }	-	{ YYYY/MM/DD }	-	{ MODIFICATIONS }
# import necessary libraries and functions
import json
import os
import requests
import traceback

from flask import Flask, jsonify, request

import data_models

# creating a Flask app
app = Flask(__name__)


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

    host = "localhost"
    if is_test or is_test is None:
        pass
    else:
        host = "172.17.0.2"

    if request.method == 'GET':
        response = Flask.response_class()
        response.content_type = "json"

        data = data_models.Log.get_logs(password, host)
        response.data = json.dumps(data, cls=data_models.DataModelJsonEncoder)

        log = data_models.Log(os.path.basename(__file__), "Logs retrieved from /logs GET", log_type="Event")
        log.create(password)
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
