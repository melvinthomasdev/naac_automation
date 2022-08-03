import cv2

import io
#import cv2
import base64 
import numpy as np
from PIL import Image

# Take in base64 string and return PIL image
def stringToImage(base64_string):
    imgdata = base64.b64decode(base64_string)
    return Image.open(io.BytesIO(imgdata))

# # convert PIL Image to an RGB image( technically a numpy array ) that's compatible with opencv
# def toRGB(image):
#     return cv2.cvtColor(np.array(image), cv2.COLOR_BGR2RGB)


# image enhacement
def enhance_image(image):
    image= stringToImage(image) 
    img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    at = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 199, 5)
    return image


# blur detection
def is_blur(image):
    image= stringToImage(image) 
    gray_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  #convert into grayscale
    laplace = cv2.Laplacian(gray_img, cv2.CV_64F).var()
    if laplace > 150:
        return False
    else:
        return True
