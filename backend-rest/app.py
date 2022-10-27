# Referred to: https://www.geeksforgeeks.org/python-build-a-rest-api-using-flask/?id=discuss
# { DEV }	-	{ YYYY/MM/DD }	-	{ MODIFICATIONS }
# import necessary libraries and functions
import json
import os

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


# BELOW ARE STUB TUTORIAL METHODS - KEEPING THEM HERE FOR LATER REFERENCE

# A simple function to calculate the square of a number
# the number to be squared is sent in the URL when we use GET
# on the terminal type: curl http://127.0.0.1:5000 / home / 10
# this returns 100 (square of 10)
@app.route('/home/<int:num>', methods=['GET'])
def disp(num):
    return jsonify({'data': num ** 2})


# driver function
if __name__ == '__main__':
    # This is important for Docker
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
