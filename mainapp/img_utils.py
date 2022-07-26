import cv2


# image enhacement
def enhance_image(image):
    img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    at = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 199, 5)
    return image


# blur detection
def is_blur(image):
    gray_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    laplace = cv2.Laplacian(gray_img, cv2.CV_64F).var()
    if laplace > 150:
        return False
    else:
        return True
