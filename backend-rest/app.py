# Referred to: https://www.geeksforgeeks.org/python-build-a-rest-api-using-flask/?id=discuss
# { DEV }	-	{ YYYY/MM/DD }	-	{ MODIFICATIONS }
# import necessary libraries and functions
import json

from flask import Flask, jsonify, request
import ResponseClasses

# creating a Flask app
app = Flask(__name__)


# http://127.0.0.1:5000/

# Get the current map data
# Note: Currently has dummy data
@app.route('/mapdata', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        response = Flask.response_class()
        response.content_type = "json"
        data = ResponseClasses.LocationResponse(1)
        response.data = json.dumps(data, cls=ResponseClasses.LocationResponseEncoder)
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
    app.run(debug=True)
