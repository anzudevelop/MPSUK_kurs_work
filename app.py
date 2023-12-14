import os
import subprocess
from PIL import Image
from flask import Flask, render_template, request, send_from_directory
from flask_ngrok import run_with_ngrok 
import random

#home_dir = os.system("fswebcam --no-banner -r 480x272 test1.jpg")
#list_files = subprocess.run(["ls"])
#os.system("fswebcam --no-banner -r 480x272 test1.jpg")

app = Flask(__name__)
#run_with_ngrok(app)


pwm = random.random()
noPhoto = True

def calculate_brightness(image):
    greyscale_image = image.convert('L')
    histogram = greyscale_image.histogram()
    pixels = sum(histogram)
    brightness = scale = len(histogram)

    for index in range(0, scale):

        ratio = histogram[index] / pixels
        brightness += ratio * (-scale + index)
    return 1 if brightness == 255 else brightness / scale

def deletePhoto():
    os.system("rm filename image.jpg")
    global noPhoto
    noPhoto = True
# image1 = Image.open("test1.jpg")
# image2 = Image.open("test2.jpg")
# image3 = Image.open("test3.jpg")
# image_white = Image.open("white.jpg")
# image_black = Image.open("black.jpg")
# print(calculate_brightness(image1))
# print(calculate_brightness(image2))
# print(calculate_brightness(image3))
# print(calculate_brightness(image_white))
# print(calculate_brightness(image_black))

UPLOAD_FOLDER = ''

@app.route("/")
def index():
    return render_template('main.html')

@app.route("/get_image", methods=['GET', 'POST'])
def get_image():
    print("Делаю снимок")
    os.system("fswebcam --no-banner -r 480x272 image.jpg")
    global noPhoto
    noPhoto = False
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
    if(noPhoto == False):
        deletePhoto()
    return response



if __name__ == "__main__":
    #app.run()
    app.run(host='0.0.0.0', port=5555)

