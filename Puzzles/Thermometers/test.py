import string

import cv2
import easyocr

image_path = "Level_012.png"
large_img_bgr = cv2.imread(image_path, cv2.IMREAD_COLOR)
large_img_rgb = cv2.cvtColor(large_img_bgr, cv2.COLOR_BGR2RGB)
roi = large_img_rgb[200:396, 980:1180]
scale = .75
roi_large = cv2.resize(roi, None, fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)
reader = easyocr.Reader(['en'])
result = reader.readtext(roi_large, allowlist=string.digits)
print(result)