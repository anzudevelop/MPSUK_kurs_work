from PIL import Image
def calculate_brightness(image):
    greyscale_image = image.convert('L')
    histogram = greyscale_image.histogram()
    pixels = sum(histogram)
    brightness = scale = len(histogram)

    for index in range(0, scale):

        ratio = histogram[index] / pixels
        brightness += ratio * (-scale + index)
    return 1 if brightness == 255 else brightness / scale

imag1 = Image.open("test1.jpg")
imag2 = Image.open("test2.jpg")
imag3 = Image.open("test3.jpg")
imag_white = Image.open("white.jpg")
imag_black = Image.open("black.jpg")
print(calculate_brightness(imag1))
print(calculate_brightness(imag2))
print(calculate_brightness(imag3))
print(calculate_brightness(imag_white))
print(calculate_brightness(imag_black))