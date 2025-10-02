
import cv2
import easyocr


# 初始化 OCR
reader = easyocr.Reader(['en'])

# 读取图像
image_path = "Level_044.png"
img = cv2.imread(image_path, cv2.IMREAD_COLOR)
h, w, _ = img.shape

# 手动裁剪棋盘区域 (大约位置，根据你图片尺寸来微调)
y1, y2 = 200, 1380
x1, x2 = 0, 1180
board = img[y1:y2, x1:x2]

# 切分成 10x10
rows, cols = 10, 10
cell_h = (y2 - y1) // rows
cell_w = (x2 - x1) // cols

results = {}

for i in range(rows):
    for j in range(cols):
# for i in [7,8]:
#     for j in [6,7]:
        # 裁剪格子
        y_start, y_end = i * cell_h, (i + 1) * cell_h
        x_start, x_end = j * cell_w, (j + 1) * cell_w
        cell = board[y_start:y_end, x_start:x_end]
        scale = 4  # 放大 4 倍
        cell = cv2.resize(cell, None, fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)

        # 转灰度
        gray = cv2.cvtColor(cell, cv2.COLOR_BGR2GRAY)

        # cv2.imshow(f"cell {i},{j}", gray)

        # 转成 RGB 给 easyocr
        cell_rgb = cv2.cvtColor(gray, cv2.COLOR_GRAY2RGB)

        # OCR
        ocr_result = reader.readtext(cell, allowlist='?0123456789')
        texts = [(text, float(prob)) for (_, text, prob) in ocr_result]

        if texts:
            results[(i, j)] = texts

# 打印结果
for pos, texts in results.items():
    print(f"Cell {pos}: {texts}")

# cv2.waitKey(0)
# cv2.destroyAllWindows()
