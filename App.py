from flask import Flask, Response, request, send_file
import cv2
import atexit

app = Flask(__name__)
buzzer_state = "OFF"

camera = cv2.VideoCapture(0)

def generate_frames():
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    with open("App.html", "r") as f:
        html = f.read().replace("{{ buzzer_state }}", buzzer_state)
    return html

@app.route('/video')
def video():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/App.css')
def style():
    return send_file('App.css')

@app.route('/logo.png')
def logo():
    return send_file('logo.png')

@app.route('/bg.jpeg')
def bg():
    return send_file('bg.jpeg')

@app.route('/buzzer', methods=['POST'])
def control_buzzer():
    global buzzer_state
    action = request.form['action']
    if action == 'ON':
        buzzer_state = 'ON'
        print("Buzzer turned ON")
    elif action == 'OFF':
        buzzer_state = 'OFF'
        print("Buzzer turned OFF")
    return ('', 204)

@atexit.register
def cleanup():
    print("Releasing camera...")
    camera.release()

if __name__ == '__main__':
    app.run(debug=True)
