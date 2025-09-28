import cv2
import numpy as np


yoffset = 198
# Load image
img = cv2.imread('Puzzles/DesertDunes/Level_001.png')
roi = img[yoffset:1385, 0:1182]
gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray, (5, 5), 0)
edges = cv2.Canny(blur, 50, 150)

# Hough transform
linesP = cv2.HoughLinesP(
    edges,
    1,
    np.pi / 180,
    500,
    minLineLength=500,
    maxLineGap=300
)

horizontal_lines = []
vertical_lines = []

if linesP is not None:
    for line in linesP:
        x1, y1, x2, y2 = line[0]
        y1 += yoffset
        y2 += yoffset
        cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 10)

        if abs(y2 - y1) < 10:  # horizontal
            horizontal_lines.append(int((y1 + y2) / 2))
        elif abs(x2 - x1) < 10:  # vertical
            vertical_lines.append(int((x1 + x2) / 2))

# 去重（避免一条线被识别多次）
horizontal_lines = sorted(set(horizontal_lines))
vertical_lines = sorted(set(vertical_lines))

# 求交点
intersections = []
for y in horizontal_lines:
    for x in vertical_lines:
        intersections.append((x, y))
        cv2.circle(img, (x, y), 10, (0, 0, 255), -1)

print("Intersections:")
for pt in intersections:
    print(pt)

cv2.imshow("Grid Intersections", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
