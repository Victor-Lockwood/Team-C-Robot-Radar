from flask import Flask, session, render_template, Response, request, send_file, jsonify, request
import requests
import gopigo
import time
from picamera import PiCamera
from time import sleep
from camera_pi import Camera
from PIL import Image
from flask_session import Session
import easygopigo
import zipfile
import io
import pathlib


app = Flask(__name__)

SESSION_TYPE = 'filesystem'
app.config.from_object(__name__)
Session(app)

def __get_offset():
    return 5

my_ultrasonic = easygopigo.UltraSonicSensor()
servo_pos = 90
location =[2.5, 2.5]
orientation='E'
speedOffset=8#this is necessary to know what coordinate to change
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
            location = [round(location[0]+ 0.45, 2), round(location[1],2)]
        if orientation == 'N':
            location = [round(location[0],2), round(location[1] +0.45,2)]
        if orientation == 'W':
            location = [round(location[0]-0.45, 2), round(location[1],2)]
        if orientation == 'S':
            location = [round(location[0],2), round(location[1]- 0.45,2)]
    elif command == 'B':
        if orientation == 'E':
            location = [round(location[0]-0.45, 2), round(location[1],2)]
        if orientation == 'N':
            location = [round(location[0],2), round(location[1]- 0.45,2)]
        if orientation == 'W':
            location = [round(location[0]+ 0.45,2), round(location[1],2)]
        if orientation == 'S':
            location = [round(location[0],2), round(location[1] +0.45,2)]
        
            
        
            
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
            

@app.route('/')
def index():
        servo_pos = 90
        return 'Hello world'

@app.route('/forward')
def forward():
        #gopigo.turn_left_wait_for_completion(33)
        #if 'left_speed' not in globals():
        global left_speed
        left_speed = 155
            
        #if 'right_speed' not in globals():
        global right_speed
        right_speed = 150

        #print(left_speed)
        #print(right_speed)
        
        gopigo.set_left_speed(left_speed)
        gopigo.set_right_speed(right_speed)
        
        print("Forward!")
        gopigo.fwd(50)#)+ speedOffset)  # Send the GoPiGo Forward
        sleep(2.5)
        determineLocationChange('F', 'F')
        #sleep(2.5)
        print("location: ", str(location), ", orientation: ", str(orientation))
        #gopigo.stop()  # the stop the GoPiGo
        data = my_ultrasonic.read()
        #print("data: ", str(data))
       
        #data = my_ultrasonic.read()
        
        
        #motor_pulses_left = gopigo.enc_read(0)
        #motor_pulses_right = gopigo.enc_read(1)
        #print(motor_pulses_left)
        #print(motor_pulses_right)
        '''
        if(motor_pulses_right > motor_pulses_left):
            left_speed += __get_offset()
        elif (motor_pulses_left > motor_pulses_right):
            right_speed += __get_offset()
        '''       
        #print("left motor speed: " + str(left_speed))
        #print("right motor speed: " + str(right_speed))
        
        return jsonify(location = location , orientation = orientation, radar = data)

@app.route('/backward')
def backward():
        print("Backward!")
        gopigo.bwd(50)  # Send the GoPiGo Backward
        #sleep(2.5)
        determineLocationChange('F', 'B')
        print("location: ", str(location), ", orientation: ", str(orientation))
        #gopigo.stop()  # and then stop the GoPiGo.
        data = my_ultrasonic.read()
        return jsonify(location = location , orientation = orientation, radar = data)        

@app.route('/left')
def left():
        print("Left!")
        gopigo.turn_left_wait_for_completion(100)
        #sleep(2.5)
        determineLocationChange('T', 'L')
        print("location: ", str(location), ", orientation: ", str(orientation))
        #gopigo.stop()
        data = my_ultrasonic.read()
        return jsonify(location= location , orientation = orientation, radar = data)

@app.route('/right')
def right():
        print("Right!")
        gopigo.turn_right_wait_for_completion(100)
        #sleep(2.5)
        determineLocationChange('T', 'R')
        print("location: ", str(location), ", orientation: ", str(orientation))
        #gopigo.stop()
        data = my_ultrasonic.read()
        return jsonify(location= location , orientation = orientation, radar = data)
    
@app.route('/camera', methods=['GET','POST'])
def takePicture():
        if request.method == 'POST':
            print("Picture Taken!")
            camera = PiCamera()
            camera.start_preview()
            sleep(2.5)
            camera.capture('/home/pi/Desktop/pictures/frontPicture.png')
            gopigo.turn_right_wait_for_completion(90)
            sleep(2.5)
            camera.capture('/home/pi/Desktop/pictures/ninetyDegreesPicture.png')
            gopigo.turn_right_wait_for_completion(90)
            sleep(2.5)
            camera.capture('/home/pi/Desktop/pictures/oneEightyDegreesPicture.png')
            gopigo.turn_right_wait_for_completion(90)
            sleep(2.5)
            camera.capture('/home/pi/Desktop/pictures/twoSeventyDegreesPicture.png')
            gopigo.turn_right_wait_for_completion(90)
            sleep(2.5)
            camera.stop_preview()
            camera.close()
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
            camera.close()
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
    
    #gopigo.set_left_speed(100)
    #gopigo.set_right_speed(170)
    print(gopigo.read_motor_speed)
    
    #gopigo.set_speed(150)
    
    
    lst=[]
    lst = stk.split(",")
    for i in  lst:
        if(i == 'f'):
            gopigo.fwd(100)
            determineLocationChange('F', 'F')
            sleep(2.5)
            #gopigo.stop()
            #time.sleep(.25)
        if(i == 'b'):
            gopigo.bwd(100)
            determineLocationChange('F', 'B')
            sleep(2.5)
            #gopigo.stop()
            #time.sleep(.25)
        if(i == 'r'):
            gopigo.turn_right_wait_for_completion(100)
            determineLocationChange('T', 'R')
            sleep(2.5)
            #gopigo.stop()
            #time.sleep(.25)
        if(i == 'l'):
            gopigo.turn_left_wait_for_completion(100)
            determineLocationChange('T', 'L')
            sleep(2.5)
            #gopigo.stop()
            #time.sleep(.25)
        sleep(2.5)
        gopigo.stop()
    data = my_ultrasonic.read()
    return jsonify(location= location , orientation = orientation, radar = data)
    


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
    
@app.route('/liveStream', methods=['GET', 'POST'])
def liveStream():
    if request.method == 'POST':
        camera = PiCamera()
        camera.start_preview()
        #sleep(2.5)
        camera.capture('/home/pi/Desktop/pictures/videoFeed.png')
        camera.stop_preview()
        camera.close()
            
        return send_file('/home/pi/Desktop/pictures/videoFeed.png', mimetype='image/png')   
        #return send_file(data, mimetype='application/zip', as_attachment=True, attachment_filename='data.zip')
        
    if request.method == 'GET':
        return "use post"
        #return render_template('pi_camera_index.html')
 #this simply tests our connection w/ remote, things are good if a 200 returns
@app.route('/logMoxie')
def logMoxie():
    url = 'http://<REMOTE IP>:9823/logs?password=<PASSWORD>&remote=True'
    data = requests.get(url)#request.form.get('origin')
    print("Data: ",data)
    return str(data)


    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)#9871)#debug = False, host = '0.0.0.0')