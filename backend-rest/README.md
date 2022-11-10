# Backend Rest

## API Specification

### /initialize

#### GET
For the robot to hit so its public IP can be stored in the `robot_ip` session
variable.

- Returns
  - `Got IP` (string value)
- URL Parameters
  - None

### /checkip

#### GET
Returns the IP of the robot stored in the session, if available.

- Returns
  - Stored robot public IP as a string
  - Empty string if unavailable
- URL Parameters
  - None

### /panoramic
***UNDER CONSTRUCTION***

Get a stitched together panoramic of pictures the robot takes
facing North, South, East and West

#### GET
- Returns
  - Image of type `.png`
- URL Parameters
  - None


### /mapdata

#### GET



- Returns
  - JSON object of a list of MapObjects
  - Sample JSON:
  ```json
  [
      {
          "map_id": 1,
          "object_type": "Can",
          "location": [
              1,
              5
          ],
          "created_at": "2022-11-04T12:41:17.564674",
          "direction": null,
          "obj_id": 4
      }
  ]
  ```
- URL Parameters
  - *mapid*
    - Id of the Map the returned objects are associated with.
  - *objtype*
    - The type of MapObject to be returned.  Valid values are
    `Can`, `OtherRobot` and `OurRobot`
  - *istest*
    - If this is a local endpoint meant to use a local 
    Docker database (`True` or `False`). Optional, defaults to `False`
  - *password*
    - Password for `flaskuser`.
  - *remote*
    - Connect to the Docker DB on Moxie (`True` or `False`).  
    Optional, defaults to `False`.

#### POST
Creates a new Map and sets its id to the session variable `current_map_id`.
- Returns
  - `New Map ID: <Map Id>`
- URL Parameters
  - None

### /move
***UNDER CONSTRUCTION***

#### GET
Moves the robot in the specified direction, updates its location as well as 
saves any new obstacles detected.

- Returns
  - ***UNDER CONSTRUCTION***
- URL Parameters
  - *movekey*
    - Key pressed for movement.  Valid values are `W` (move forward), `A` (turn left),
    `S` (move backward) or `D` (turn right).  
  - *istest*
    - If this is a local endpoint meant to use a local 
    Docker database (`True` or `False`). Optional, defaults to `False`
  - *password*
    - Password for `flaskuser`.
  - *remote*
    - Connect to the Docker DB on Moxie (`True` or `False`).  
    Optional, defaults to `False`.

### /testrobotconnect

#### GET
Checks to see if the robot is reachable by sending a request for it to run right.

- Returns
  - Success:
    - `Test connect to robot successful!` (string)
  - Failure:
    - `Could not reach robot.` (string)
- URL Parameters
  - None

### /logs

#### GET
Returns a list of JSON-formatted logs from the database.

- Returns
  - Success (sample JSON):
  ```json
  [
    {
        "created_at": "2022-11-04T14:05:32.478150",
        "origin": "app.py",
        "message": "invalid integer value \"localhost\" for connection option \"port\"\n",
        "log_type": "Error",
        "stack_trace": "",
        "id": 10
    },
    {
        "created_at": "2022-11-04T14:07:12.071802",
        "origin": "app.py",
        "message": "Logs retrieved from /logs GET",
        "log_type": "Event",
        "stack_trace": "",
        "id": 11
    }
  ]
  ```
  - Failure:
    - `An error occurred - see logs` (string)
- URL Parameters
  - None

### /autonomous
***UNDER CONSTRUCTION***

#### POST
Receives a set of Dijkstra-calculated coordinates to be translated into movements
to send to the robot.

- Request Body Structure 
  ```json
    {
       "Coordinates":
        [
           [15, 1],
           [15, 2],
           [15, 3],
           [15, 4],
           [15, 5],
           [15, 6],
           [15, 7],
           [15, 8],
           [15, 9]
       ]
    }
  ```
- Returns
  - `***UNDER CONSTRUCTION***
- URL Parameters
  - ***UNDER CONSTRUCTION***

## Creating Docker Image and Testing Locally
Make sure you have Docker installed!

To get testing:
1. Run `docker build -t flask-app-backend . `
2. Run `docker run -p 9823:5000 -d flask-app-backend`
3. Hit `http://localhost:9823/logs?password=<password>&istest=False` in either Postman or your
browser.  If it works, everything built correctly!