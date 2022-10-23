# Referred to: https://www.geeksforgeeks.org/python-build-a-rest-api-using-flask/?id=discuss
# { DEV }	-	{ YYYY/MM/DD }	-	{ MODIFICATIONS }
# import necessary libraries and functions
import json
import os

from flask import Flask, jsonify, request

import ResponseClasses
import init_db

# creating a Flask app
app = Flask(__name__)


# http://localhost:5000/mapdata

# Get the current map data
# Note: Currently has dummy data
@app.route('/mapdata', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        response = Flask.response_class()
        response.content_type = "json"
        data = ResponseClasses.LocationResponse(1)
        response.data = json.dumps(data, cls=ResponseClasses.LocationResponseEncoder)

        init_db.db_init_test()
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



