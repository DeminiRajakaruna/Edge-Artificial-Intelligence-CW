from flask import Flask, request, jsonify
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
import smtplib
import requests
from email.message import EmailMessage
import os

app = Flask(__name__)
model = load_model('elephant_detection_model.h5')

ESP32_URL = 'http://192.168.1.7'
EMAIL_RECEIVER = 'you@example.com'

def send_email():
    msg = EmailMessage()
    msg.set_content("Elephant detected!")
    msg['Subject'] = "Alert: Elephant Detected"
    msg['From'] = "alert@example.com"
    msg['To'] = EMAIL_RECEIVER

    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.starttls()
        smtp.login("your_email", "your_password")
        smtp.send_message(msg)

def is_elephant(img_path):
    img = image.load_img(img_path, target_size=(224, 224))  # adjust to model
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    pred = model.predict(x)
    return pred[0][0] > 0.5  # adjust threshold

@app.route('/api/upload', methods=['POST'])
def upload():
    img_file = request.files['image']
    path = './uploaded.jpg'
    img_file.save(path)

    if is_elephant(path):
        requests.get(f'{ESP32_URL}/buzzer/on')  # activate buzzer
        send_email()
        return jsonify({'elephant': True})
    return jsonify({'elephant': False})

if __name__ == '__main__':
    app.run(debug=True)
