import os

import cv2
import easyocr
import numpy as np

from Puzzles.common import analyze_horizontal_line, analyze_vertical_line, process_pixel_long_results, recognize_digits, \
    level_node_string, to_hex_char, normalize_lines, recognize_grid_lines, get_levels_str_from_puzzle

reader = easyocr.Reader(['en'])  # 初始化，只加载英文模型

def _recognize_digits(
        large_img: np.ndarray,
        horizontal_line_list: list[tuple[int, int]],
        vertical_line_list: list[tuple[int, int]]
) -> list[list[str]]:
    gray = cv2.cvtColor(large_img, cv2.COLOR_BGR2GRAY)
    _, img_result = cv2.threshold(gray, 250, 255, cv2.THRESH_BINARY)

    result = []
    for row_idx, (y, h) in enumerate(vertical_line_list):
        row_result = []
        for col_idx, (x, w) in enumerate(horizontal_line_list):
            # 裁剪感兴趣区域(ROI)
            roi = img_result[y:y + h, x:x + w]
            roi_large = cv2.resize(roi, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)

            output = reader.readtext(roi_large, detail=0)
            if output and output[0] == '22':
                output = reader.readtext(roi, detail=0)
            text = output[0] if output else ' '

            # 将识别的结果添加到当前行的结果列表中
            row_result.append(text)

        # 将当前行的结果添加到最终结果列表中
        result.append(row_result)

    return result


def _format_digit_matrix(matrix):
    lines = []
    for row_str in matrix:
        line = ''
        for col_str in row_str:
            line += to_hex_char(col_str)
        lines.append(line + '`')
    result = '\n'.join(lines)
    return result


def _get_level_str_from_image(large_img: np.ndarray) -> str:
    processed_horizontal_lines, processed_vertical_lines = recognize_grid_lines(large_img)
    digits_matrix = _recognize_digits(large_img, processed_horizontal_lines, processed_vertical_lines)
    level_str = _format_digit_matrix(digits_matrix)
    return level_str


get_levels_str_from_puzzle("DesertDunes", 1, 200, _get_level_str_from_image)
