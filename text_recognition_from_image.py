import cv2
import numpy as np
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r"your installation folder"


img = cv2.imread("your image path")
img = cv2.resize(img, None, fx=0.5, fy=0.5)

text = pytesseract.image_to_string(img)

print(text)
cv2.imshow("img", img)
cv2.waitKey(0)