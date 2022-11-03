from flask import Flask, render_template, Response, request, send_file, jsonify
import gopigo
import time
from picamera import PiCamera
from time import sleep
from camera_pi import Camera
from PIL import Image
import easygopigo
import zipfile
import io
import pathlib


my_ultrasonic = easygopigo.UltraSonicSensor()
servo_pos = 90
location =[2.5, 2.5]
orientation='E'#this is necessary to know what coordinate to change
#E will mean the pi is facing the east
#N north
#S south
#W west
#used to determine the change in location coordinates and orientation change
def determineLocationChange(orientationChange = 'F', command = 'N'):
    global orientation
    global location
    if orientationChange == 'T':
        print("you want to change the orientation")
        if command == 'R':
            if orientation == 'E':
                orientation =='S'
            elif orientation == 'N':
                orientation = 'E'
            elif orientation == 'W':
                orientation = 'N'
            elif orientation == 'S':
                orientation = 'W'
        elif command == 'L':
            if orientation == 'E':
                orientation = 'N'
            elif orientation == 'N':
                orientation = 'W'
            elif orientation == 'W':
                orientation = 'S'
            elif orientation == 'S':
                orientation = 'E'
                
    
    #we need to determine what the command is and based on that change the location
    #coordinates as necessary, for example im the robot is facing north, can the backward
    #command is called, we will drop the y value by 0.01
    #if the robot needs to change location and orientation
    
    if command == 'N':
        pass
    elif command == 'F':
        if orientation == 'E':
            location = [round(location[0]+ 0.01, 2), round(location[1],2)]
        if orientation == 'N':
            location = [round(location[0],2), round(location[1] +0.01,2)]
        if orientation == 'W':
            location = [round(location[0]-0.01, 2), round(location[1],2)]
        if orientation == 'S':
            location = [round(location[0],2), round(location[1]- 0.01,2)]
    elif command == 'B':
        if orientation == 'E':
            location = [round(location[0]-0.01, 2), round(location[1],2)]
        if orientation == 'N':
            location = [round(location[0],2), round(location[1]- 0.01,2)]
        if orientation == 'W':
            location = [round(location[0]+ 0.01,2), round(location[1],2)]
        if orientation == 'S':
            location = [round(location[0],2), round(location[1] +0.01,2)]
        
            
        
            
    '''
    if changeLocation == 'Y':
        if orientation == 'E':
            location = [location[0]+ 0.01, location[1]]
        elif orientation == 'S':
            location = [location[0], location[1]- 0.01]
        elif orientation == 'W':
            location = [location[0]-0.01, location[1]]
        else:
            location = [location[0], location[1] +0.01]
    '''
            
        
    

app = Flask(__name__)

@app.route('/')
def index():
        servo_pos = 90
        return 'Hello world'

@app.route('/forward')
def forward():
        print("Forward!")
        gopigo.fwd(100) # Send the GoPiGo Forward
        determineLocationChange('F', 'F')
        sleep(2.5)
        print("location: ", str(location), ", orientation: ", str(orientation))
        gopigo.stop()   # the stop the GoPiGo
        data = my_ultrasonic.read()
        return jsonify(['location', location , 'orientation',orientation, 'radar', data])

@app.route('/backward')
def backward():
        print("Backward!")
        gopigo.bwd(100) # Send the GoPiGo Backward
        sleep(2.5)
        determineLocationChange('F', 'B')
        print("location: ", str(location), ", orientation: ", str(orientation))
        gopigo.stop()   # and then stop the GoPiGo.
        data = my_ultrasonic.read()
        return jsonify(['location', location , 'orientation',orientation, 'radar', data])
        

@app.route('/left')
def left():
        print("Left!")
        gopigo.turn_left_wait_for_completion(100)
        sleep(2.5)
        determineLocationChange('T', 'L')
        print("location: ", str(location), ", orientation: ", str(orientation))
        gopigo.stop()
        data = my_ultrasonic.read()
        return jsonify(['location', location , 'orientation',orientation, 'radar', data])

@app.route('/right')
def right():
        print("Right!")
        gopigo.turn_right_wait_for_completion(100)
        sleep(2.5)
        determineLocationChange('T', 'R')
        print("location: ", str(location), ", orientation: ", str(orientation))
        gopigo.stop()
        data = my_ultrasonic.read()
        return jsonify(['location', location , 'orientation',orientation, 'radar', data])
    
@app.route('/camera', methods=['GET','POST'])
def takePicture():
        if request.method == 'POST':
            print("Picture Taken!")
            camera = PiCamera()
            camera.start_preview()
            sleep(5)
            camera.capture('/home/pi/Desktop/pictures/frontPicture.png')
            gopigo.turn_right_wait_for_completion(100)
            sleep(2.5)
            camera.capture('/home/pi/Desktop/pictures/ninetyDegreesPicture.png')
            gopigo.turn_right_wait_for_completion(100)
            sleep(2.5)
            camera.capture('/home/pi/Desktop/pictures/oneEightyDegreesPicture.png')
            gopigo.turn_right_wait_for_completion(100)
            sleep(2.5)
            camera.capture('/home/pi/Desktop/pictures/twoSeventyDegreesPicture.png')
            gopigo.turn_right_wait_for_completion(100)
            sleep(2.5)
            camera.stop_preview()
            #we now must zip the four images together to be able to send it in one go
            listFiles = ['/home/pi/Desktop/pictures/frontPicture.png',
                         '/home/pi/Desktop/pictures/ninetyDegreesPicture.png',
                         '/home/pi/Desktop/pictures/oneEightyDegreesPicture.png',
                         '/home/pi/Desktop/pictures/twoSeventyDegreesPicture.png']
            data = io.BytesIO()
            with zipfile.ZipFile(data, 'w') as zipF:
                for file in listFiles:
                    zipF.write(file, compress_type=zipfile.ZIP_DEFLATED)
            data.seek(0)
            
            return send_file(data, mimetype='application/zip', as_attachment=True, attachment_filename='data.zip')
            
        else:
            camera = PiCamera()
            camera.start_preview()
            sleep(5)
            camera.capture('/home/pi/Desktop/pictures/frontPicture.png')
            gopigo.turn_right_wait_for_completion(100)
            sleep(2.5)
            camera.capture('/home/pi/Desktop/pictures/ninetyDegreesPicture.png')
            gopigo.turn_right_wait_for_completion(100)
            sleep(2.5)
            camera.capture('/home/pi/Desktop/pictures/oneEightyDegreesPicture.png')
            gopigo.turn_right_wait_for_completion(100)
            sleep(2.5)
            camera.capture('/home/pi/Desktop/pictures/twoSeventyDegreesPicture.png')
            gopigo.turn_right_wait_for_completion(100)
            sleep(2.5)
            camera.stop_preview()
            listFiles = ['/home/pi/Desktop/pictures/frontPicture.png',
                         '/home/pi/Desktop/pictures/ninetyDegreesPicture.png',
                         '/home/pi/Desktop/pictures/oneEightyDegreesPicture.png',
                         '/home/pi/Desktop/pictures/twoSeventyDegreesPicture.png']
            data = io.BytesIO()
            with zipfile.ZipFile(data, 'w') as zipF:
                for file in listFiles:
                    zipF.write(file, compress_type=zipfile.ZIP_DEFLATED)
            data.seek(0)
            
            return send_file(data, mimetype='application/zip', as_attachment=True, attachment_filename='data.zip')
            
            #return 'Use Post'


@app.route('/dance')
def dance():
    print("Dance!")
    for each in range(0,5):
        gopigo.right()
        time.sleep(0.25)
        gopigo.left()
        time.sleep(0.25)
        gopigo.bwd()
        time.sleep(0.25)
    gopigo.stop()
    return 'Dance!'

@app.route('/coffee')
def coffee():
    print("Coffee!")
    return 'coffee!'

@app.route('/radar')
def radar():
        data = my_ultrasonic.read()
        return str(data)
       

@app.route('/autonomous/<string:stk>')
def autonomous(stk):
    #need to offset by 5 to incorporate hardware differences
    gopigo.set_left_speed(105)
    gopigo.set_right_speed(100)
    
    lst=[]
    lst = stk.split(",")
    for i in  lst:
        if(i == 'f'):
            gopigo.fwd(100)
            determineLocationChange('F', 'F')
            #sleep(1000)
            #gopigo.stop()
            #time.sleep(.25)
        if(i == 'b'):
            gopigo.bwd(100)
            determineLocationChange('F', 'B')
            #sleep(1000)
            #gopigo.stop()
            #time.sleep(.25)
        if(i == 'r'):
            gopigo.turn_right_wait_for_completion(100)
            determineLocationChange('T', 'R')
            #sleep(1000)
            #gopigo.stop()
            #time.sleep(.25)
        if(i == 'l'):
            gopigo.turn_left_wait_for_completion(100)
            determineLocationChange('T', 'L')
            #sleep(1000)
            #gopigo.stop()
            #time.sleep(.25)
        sleep(2.5)
        #gopigo.stop()
    data = my_ultrasonic.read()
    return jsonify(['location', location , 'orientation',orientation, 'radar', data])
    


@app.route('/moveServo/<string:inp>')
def moveServo(inp):
        global servo_pos
        if inp=='a':
            servo_pos=servo_pos+10  # If input is 'a' move the servo forward 10 degrees.
        elif inp=='d':
            servo_pos=servo_pos-10  # If the input is 'd' move the servo backward by 10 degrees.
        elif inp=='s':
            servo_pos=90            
        
    #Get the servo angles back to the normal 0 to 180 degree range
        if servo_pos>180:
            servo_pos=180
        if servo_pos<0:
            servo_pos=0
        
        gopigo.servo(servo_pos)     # This function updates the servo with the latest positon.  Move the servo.
        time.sleep(.1)
        return 'servo position: ' + str(servo_pos)
@app.route('/liveStream')
def liveStream():

        return render_template('pi_camera_index.html')
    
def gen(camera):
    # Video streaming generator function.  For more on generator functions see Miguel Gringberg's beautiful post here:  https://blog.miguelgrinberg.com/post/video-streaming-with-flask
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/liveStream/video_feed')
def video_feed():
    # Video streaming route. Put this in the src attribute of an img tag.
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


        
    
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
