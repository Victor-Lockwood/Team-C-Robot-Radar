from flask import Flask, render_template, Response
import gopigo
import time
from picamera import PiCamera
from time import sleep
from camera_pi import Camera

servo_pos = 90

app = Flask(__name__)

@app.route('/')
def index():
        servo_pos = 90
        return 'Hello world'

@app.route('/forward')
def forward():
	print("Forward!")
	gopigo.fwd()	# Send the GoPiGo Forward
	time.sleep(1)	# for 1 second.
	gopigo.stop()	# the stop the GoPiGo
	return 'Alexabot moved forward!'

@app.route('/backward')
def backward():
	print("Backward!")
	gopigo.bwd()	# Send the GoPiGo Backward
	time.sleep(1)	# for 1 second
	gopigo.stop()	# and then stop the GoPiGo.
	return 'Backward!'

@app.route('/left')
def left():
	print("Left!")
	gopigo.left()
	time.sleep(1)
	gopigo.stop()
	return 'Left!'

@app.route('/right')
def right():
	print("Right!")
	gopigo.right()
	time.sleep(1)
	gopigo.stop()
	return 'Right!'
    
@app.route('/camera')
def takePicture():
        print("Picture Taken!")
        camera = PiCamera()
        camera.start_preview()
        sleep(5)
        camera.capture('/home/pi/Desktop/pictures/newPicture.jpg')
        camera.stop_preview()
        return 'Picture Taken!'


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

@app.route('/autonomous/<string:stk>')
def autonomous(stk):
    lst=[]
    lst = stk.split(",")
    for i in lst:
        if(i == 'f'):
            gopigo.fwd(100)#in cm's
            time.sleep(.25)
        if(i == 'b'):
            gopigo.bwd(100)#in cm's
            time.sleep(.25)
        if(i == 'r'):
            gopigo.turn_right_wait_for_completion(90)#in degrees
            time.sleep(.25)
        if(i == 'l'):
            gopigo.fwd(90)#in degrees
            time.sleep(.25)            
        
    return "1st value: " + str(lst)
    


@app.route('/moveServo/<string:inp>')
def moveServo(inp):
        global servo_pos
        if inp=='a':
            servo_pos=servo_pos+10	# If input is 'a' move the servo forward 10 degrees.
        elif inp=='d':
            servo_pos=servo_pos-10	# If the input is 'd' move the servo backward by 10 degrees.
        elif inp=='s':
            servo_pos=90			
		
	#Get the servo angles back to the normal 0 to 180 degree range
        if servo_pos>180:
            servo_pos=180
        if servo_pos<0:
            servo_pos=0
		
        gopigo.servo(servo_pos)		# This function updates the servo with the latest positon.  Move the servo.
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