import string

import cv2
import easyocr

image_path = "Level_090.png"
large_img_bgr = cv2.imread(image_path, cv2.IMREAD_COLOR)
large_img_rgb = cv2.cvtColor(large_img_bgr, cv2.COLOR_BGR2RGB)
cell_length = 1180 // 7
x = cell_length * 6
y = 200
roi = large_img_rgb[y:y+cell_length, x:x+cell_length]
scale = 1.5
roi_large = cv2.resize(roi, None, fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)
reader = easyocr.Reader(['en'])
result = reader.readtext(roi_large, allowlist=string.digits)
print(result)