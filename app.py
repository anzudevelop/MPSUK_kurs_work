#pip install Flask
#pip install --upgrade Pillow
import os
from PIL import Image
from flask import Flask, render_template, request, send_from_directory

app = Flask(__name__)


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


@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route("/get_image", methods=['GET', 'POST'])
def get_image():
    if request.method == 'GET':
        print("Отправка фото...")
        return send_from_directory(UPLOAD_FOLDER, 'image.jpg')





app.run(host='0.0.0.0', port=5555)