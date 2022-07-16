import cv2

# image enhacement
def image_enhacement(image):
  img = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
  at = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,199,5)
  return image


# blur detection
def blur_detection(image):
  gray_img = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
  laplace = cv2.Laplacian(gray_img,cv2.CV_64F).var()
  if laplace>150:
        status = "Non Blurry"
  else:
        status = "Blurry"
  return status
