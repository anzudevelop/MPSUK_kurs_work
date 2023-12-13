#pip install Flask
#pip install --upgrade Pillow
#pip install flask-ngrok
import os
from PIL import Image
from flask import Flask, render_template, request, send_from_directory
from flask_ngrok import run_with_ngrok 
import random

app = Flask(__name__)
run_with_ngrok(app)

pwm = random.random()

def calculate_brightness(image):
    greyscale_image = image.convert('L')
    histogram = greyscale_image.histogram()
    pixels = sum(histogram)
    brightness = scale = len(histogram)

    for index in range(0, scale):

        ratio = histogram[index] / pixels
        brightness += ratio * (-scale + index)
    return 1 if brightness == 255 else brightness / scale

image1 = Image.open("test1.jpg")
image2 = Image.open("test2.jpg")
image3 = Image.open("test3.jpg")
image_white = Image.open("white.jpg")
image_black = Image.open("black.jpg")
print(calculate_brightness(image1))
print(calculate_brightness(image2))
print(calculate_brightness(image3))
print(calculate_brightness(image_white))
print(calculate_brightness(image_black))

UPLOAD_FOLDER = 'img'


@app.route("/")
def index():
    return render_template('main.html')

@app.route("/get_image", methods=['GET', 'POST'])
def get_image():
    if request.method == 'GET':
        print("Отправка фото...")
        return send_from_directory(UPLOAD_FOLDER, 'image.jpg')

@app.route("/logs", methods=['GET'])
def logs():
    global pwm
    print("pwm = " + str(pwm))
    response = app.response_class(
        response = str(pwm),
        status = 200,
        mimetype='text/html'
    )
    return response



if __name__ == "__main__":
    app.run()










'''
@app.route("/getGpioState", methods=["get"])
def getGpioState():
    pin = request.args.get('pin')
    global gpioState
    if gpioState:
        state = "on"
    else:
        state = "off"
    print("gpio pin " + pin + " state = " + state)
     
    response = app.response_class(
        response = state,
        status = 200,
        mimetype='text/html'
    )
    return response

@app.route("/setStringToFile", methods=["post"])
def setStringToFile():
    data = request.get_json()
    text = data.get('text')
    print("new text to file is: " + text)
    file = open('text.txt', 'w')
    file.write(text)
    file.close()
    response = app.response_class(
        response = 'ok',
        status = 200,
        mimetype='text/html'
    )
    return response
'''