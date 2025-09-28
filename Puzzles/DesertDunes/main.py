import os

import cv2
import easyocr
import numpy as np

from Puzzles.common import analyze_horizontal_line, analyze_vertical_line, process_pixel_long_results, recognize_digits, \
    level_node_string, to_hex_char, normalize_lines

yoffset = 198
def get_processed_lines(image_path: str):
    img = cv2.imread(image_path)
    roi = img[yoffset:1385, 0:1182]
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blur, 50, 150)
    linesP = cv2.HoughLinesP(
        edges,
        1,
        np.pi / 180,
        500,
        minLineLength=500,
        maxLineGap=300
    )
    y_list = []
    x_list = []
    if linesP is not None:
        for line in linesP:
            x1, y1, x2, y2 = line[0]
            y1 += yoffset
            y2 += yoffset
            if abs(y2 - y1) < 10:  # horizontal
                y_list.append(int((y1 + y2) / 2))
            elif abs(x2 - x1) < 10:  # vertical
                x_list.append(int((x1 + x2) / 2))

    y_list = sorted(set(y_list))
    x_list = sorted(set(x_list))
    y_list2 = []
    x_list2 = []
    for idx, y in enumerate(y_list):
        if idx == 0 or y - y_list[idx - 1] > 10:
            y_list2.append(y)
    for idx, x in enumerate(x_list):
        if idx == 0 or x - x_list[idx - 1] > 10:
            x_list2.append(x)
    if (1181 - x_list2[-1]) > 100:
        x_list2.append(1181)

    processed_vertical_lines = []
    for idx, y in enumerate(y_list2):
        if idx < len(y_list2) - 1:
            processed_vertical_lines.append((y, y_list2[idx + 1] - y))
    processed_horizontal_lines = []
    for idx, x in enumerate(x_list2):
        if idx < len(x_list2) - 1:
            processed_horizontal_lines.append((x, x_list2[idx + 1] - x))
    return processed_horizontal_lines, processed_vertical_lines

def recognize_digits2(
        image_path: str,
        line_list: list[tuple[int, int]],
        column_list: list[tuple[int, int]]
) -> list[list[str]]:
    # 读取图像
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, img_result = cv2.threshold(gray, 250, 255, cv2.THRESH_BINARY)

    result = []
    reader = easyocr.Reader(['en'])  # 初始化，只加载英文模型
    for row_idx, (y, h) in enumerate(column_list):
        row_result = []
        for col_idx, (x, w) in enumerate(line_list):
            # 裁剪感兴趣区域(ROI)
            roi = img_result[y:y + h, x:x + w]
            roi_large = cv2.resize(roi, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)

            output = reader.readtext(roi_large, detail=0)
            if output and output[0] == '22':
                output = reader.readtext(roi, detail=0)
            text = ' ' if not output else output[0]

            # 将识别的结果添加到当前行的结果列表中
            row_result.append(text)

        # 将当前行的结果添加到最终结果列表中
        result.append(row_result)

    return result


def format_digit_matrix(matrix):
    lines = []
    for row_str in matrix:
        line = ''
        for col_str in row_str:
            line += to_hex_char(col_str)
        lines.append(line + '`')
    result = '\n'.join(lines)
    return result


def get_level_str_from_image(image_path: str) -> str:
    processed_horizontal_lines, processed_vertical_lines = get_processed_lines(image_path)
    digits_matrix = recognize_digits2(image_path, processed_horizontal_lines, processed_vertical_lines)
    level_str = format_digit_matrix(digits_matrix)
    return level_str

def main():
    level_image_path = os.path.expanduser("~/Documents/Programs/Games/100LG/Levels/DesertDunes/")
    START_LEVEL = 1  # 起始关卡: 从1开始
    END_LEVEL = 200  # 结束关卡号
    with open(f"Levels.txt", "w") as text_file:
        for i in range(START_LEVEL, END_LEVEL+1):
            # 图像信息
            image_path = f'{level_image_path}Level_{i:03d}.png'
            print("正在处理图片 " + image_path)
            level_str = get_level_str_from_image(image_path)
            node = level_node_string(i, level_str)
            text_file.write(node)


# --- 主程序 ---
if __name__ == "__main__":
    main()
