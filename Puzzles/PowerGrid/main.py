import os

import cv2
import easyocr
import numpy as np

from Puzzles.common import analyze_horizontal_line, analyze_vertical_line, process_pixel_long_results, \
    level_node_string, recognize_text

reader = easyocr.Reader(['en'])  # 初始化，只加载英文模型

def _recognize_digits(
        large_img: np.ndarray,
        horizontal_line_list: list[tuple[int, int]],
        vertical_line_list: list[tuple[int, int]]
) -> list[list[str]]:
    result = []
    for row_idx, (y, h) in enumerate(vertical_line_list):
        row_result = []
        is_hint_row = row_idx == len(vertical_line_list) - 1
        for col_idx, (x, w) in enumerate(horizontal_line_list):
            is_hint_col = col_idx == len(horizontal_line_list) - 1
            if is_hint_row or is_hint_col:
                ch = recognize_text(reader, large_img, x, y, w, h) or ' '
            else:
                ch = ' '
            row_result.append(ch)
        result.append(row_result)
    return result

def _format_matrix(matrix):
    lines = []
    for row_idx, row in enumerate(matrix):
        line = ''.join(row)
        lines.append(line + '`')

    # 合并为多行字符串
    result = '\n'.join(lines)
    return result

def _get_level_str_from_image(large_img: np.ndarray) -> str:
    horizontal_line_results = analyze_horizontal_line(large_img, y_coord=210, start_x=0, end_x=1180)
    processed_horizontal_lines = process_pixel_long_results(horizontal_line_results, is_horizontal=True, threshold=40)
    vertical_line_results = analyze_vertical_line(large_img, x_coord=10, start_y=200, end_y=1380)
    processed_vertical_lines = process_pixel_long_results(vertical_line_results, is_horizontal=False, threshold=40)
    digits_matrix = _recognize_digits(large_img, processed_horizontal_lines, processed_vertical_lines)
    level_str = _format_matrix(digits_matrix)
    return level_str


def main():
    with open(f"Levels.txt", "w"):
        pass
    level_image_path = os.path.expanduser("~/Documents/Programs/Games/100LG/Levels/PowerGrid/")
    START_LEVEL = 1  # 起始关卡: 从1开始
    END_LEVEL = 220  # 结束关卡号
    for i in range(START_LEVEL, END_LEVEL+1):
        # 图像信息
        image_path = f'{level_image_path}Level_{i:03d}.png'
        print("正在处理图片 " + image_path)
        large_img = cv2.imread(image_path, cv2.IMREAD_COLOR)
        if large_img is None:
            print(f"错误：无法加载图像文件。{image_path}")
            continue
        level_str = _get_level_str_from_image(large_img)
        node = level_node_string(i, level_str)
        with open(f"Levels.txt", "a") as text_file:
            text_file.write(node)

# --- 主程序 ---
if __name__ == "__main__":
    main()
