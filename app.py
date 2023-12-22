import os
import subprocess
from PIL import Image
from flask import Flask, render_template, request, send_from_directory
from flask_ngrok import run_with_ngrok 
import random
#import RPi.GPIO as GPIO
import time

GPIO_PWM_PIN = 40
FREQUENCY = 1000

#GPIO.setwarnings(False)
#GPIO.setmode(GPIO.BOARD)
#GPIO.setup(GPIO_PWM_PIN, GPIO.OUT)
#pwmOutput = GPIO.PWM(GPIO_PWM_PIN, FREQUENCY)

app = Flask(__name__)

PWM_START_VALUE = 0
pwm = PWM_START_VALUE
lastPwmValue = 0
histogramOfPhoto = []
rangeForHistogram = 0

def calculate_brightness(image):
    greyscale_image = image.convert('L')
    histogram = greyscale_image.histogram()
    pixels = sum(histogram)
    brightness = scale = len(histogram)

    for index in range(0, scale):

        ratio = histogram[index] / pixels
        brightness += ratio * (-scale + index)
    return 1 if brightness == 255 else brightness / scale

def histogram(image): #Возвращает кол-во пикселей с яркостью от 0 до 255
    print("Вычисляется гистрограмма")
    greyscale_image = image.convert('L')
    histogram = greyscale_image.histogram()
    sumValues = sum(histogram)
    for index in range(0, 256):
        histogram[index] = round((histogram[index] / sumValues) * 100)
    print("Гистрограмма вычисенна")
    print(histogram)
    return histogram
def photo():
    print("Делаю снимок")
    os.system("fswebcam --no-banner -r 480x272 image.jpg")
def ledOn():
    global pwmOutput
    global pwm
    print("Включаю подсветку")
    pwmOutput.start(pwm * 100)
def ledOff():
    global pwmOutput
    print("Выключаю подсветку")
    pwmOutput.stop()
    #GPIO.cleanup()
def checkHistogram(histogramOfPhoto):
    global rangeForHistogram
    sumOfOk = 0
    global pwm
    print("Значение ШИМ: " + str(pwm))
    print("Проверка гистограммы")
    for i in range(rangeForHistogram, 256 - rangeForHistogram):
        sumOfOk = sumOfOk + histogramOfPhoto[i]
    print("Сумма: " + str(sumOfOk))
    if(sumOfOk < 50):
        pwm += 0.1
        if(pwm >= 1):
            pwm = 1
            return True
        else:
            print("Удаляю фото")
            os.system("rm image.jpg")
            return False
    if(sumOfOk >= 50):
        return True

UPLOAD_FOLDER = ''

@app.route("/")
def index():
    return render_template('main.html')

@app.route("/get_image", methods=['GET', 'POST'])
def get_image():
    global pwm
    global PWM_START_VALUE
    global lastPwmValue
    isOkResult = False
    while isOkResult == False:   
        ledOn()
        photo()
        ledOff()
        global histogramOfPhoto
        image = Image.open("image.jpg")
        histogramOfPhoto = histogram(image)
        isOkResult = checkHistogram(histogramOfPhoto)
    print("Отправка фото...")
    lastPwmValue = pwm
    pwm = PWM_START_VALUE
    return send_from_directory(UPLOAD_FOLDER, 'image.jpg')    

@app.route("/get_histogram", methods=['GET', 'POST'])
def get_histogram():
    global histogramOfPhoto
    print("Удаляю фото")
    os.system("rm image.jpg")
    response = app.response_class(
        response = str(histogramOfPhoto),
        status = 200,
        mimetype = 'text/html'
    )
    return response

@app.route("/logs", methods=['GET'])
def logs():
    global lastPwmValue
    print("pwm = " + str(round(lastPwmValue * 100)) + "%")
    response = app.response_class(
        response = str(round(lastPwmValue * 100)),
        status = 200,
        mimetype='text/html'
    )
    return response

@app.route("/setRange", methods=['POST'])
def setRange():
    global rangeForHistogram
    data = request.get_json()
    newRange = data.get('range')
    print("new range set: " + str(newRange))
    rangeForHistogram = newRange
    response = app.response_class(
        response = rangeForHistogram,
        status = 200,
        mimetype='text/html'
    )
    return response



'''
image1 = Image.open("image.jpg")
print(histogram(image1))
'''


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5555)
