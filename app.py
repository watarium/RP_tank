from flask import *
import wiringpi, time
from camera_pi import Camera
import RPi.GPIO as GPIO

wiringpi.wiringPiSetupGpio()

right_forward = 26;
right_back = 19;
left_forward = 13;
left_back = 11;
shot_gpio = 2

wiringpi.pinMode(right_forward, 1)
wiringpi.pinMode(right_back, 1)
wiringpi.pinMode(left_forward, 1)
wiringpi.pinMode(left_back, 1)

GPIO.setmode(GPIO.BCM)
GPIO.setup(shot_gpio, GPIO.OUT)
servo = GPIO.PWM(shot_gpio, 50)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

def gen(camera):
    """Video streaming generator function."""
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/motor', methods=['POST'])
def motor():
    action = request.form['action']
    if action == 'forward':
        wiringpi.digitalWrite(right_forward, 1)
        wiringpi.digitalWrite(right_back, 0)
        wiringpi.digitalWrite(left_forward, 1)
        wiringpi.digitalWrite(left_back, 0)
    elif action == 'stop':
        wiringpi.digitalWrite(right_forward, 0)
        wiringpi.digitalWrite(right_back, 0)
        wiringpi.digitalWrite(left_forward, 0)
        wiringpi.digitalWrite(left_back, 0)
    elif action == 'left':
        wiringpi.digitalWrite(right_forward, 0)
        wiringpi.digitalWrite(right_back, 1)
        wiringpi.digitalWrite(left_forward, 1)
        wiringpi.digitalWrite(left_back, 0)
    elif action == 'right':
        wiringpi.digitalWrite(right_forward, 1)
        wiringpi.digitalWrite(right_back, 0)
        wiringpi.digitalWrite(left_forward, 0)
        wiringpi.digitalWrite(left_back, 1)
    elif action == 'back':
        wiringpi.digitalWrite(right_forward, 0)
        wiringpi.digitalWrite(right_back, 1)
        wiringpi.digitalWrite(left_forward, 0)
        wiringpi.digitalWrite(left_back, 1)
    elif action == 'shot':
        servo.start(0.0)
        servo.ChangeDutyCycle(12)
        time.sleep(3)
        servo.ChangeDutyCycle(6)
        servo.stop()
    return render_template("index.html")

@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(Camera()), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True)
