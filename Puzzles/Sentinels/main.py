# import sys
# import os

# # 获取项目根目录的绝对路径
# current_file = os.path.abspath(__file__)
# sentinels_dir = os.path.dirname(current_file)
# puzzles_dir = os.path.dirname(sentinels_dir)
# project_root = os.path.dirname(puzzles_dir)

# # 添加项目根目录到 Python 路径
# sys.path.insert(0, project_root)

# print(f"Project root: {project_root}")
# print(f"Python path: {sys.path}")

import cv2
import easyocr
import numpy as np

from Puzzles.common import analyze_horizontal_line, analyze_vertical_line, process_pixel_long_results, \
    get_levels_str_from_puzzle, to_hex_char

reader = easyocr.Reader(['en'])  # 初始化，只加载英文模型


def _recognize_text(large_img: np.ndarray, x: int, y: int, w: int, h: int) -> str:
    roi = large_img[y:y + h, x:x + w]
    roi_large = cv2.resize(roi, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    output = reader.readtext(roi_large)
    if output:
        _, text, prob = output[0]
        ch = '2' if text == "22" and prob < 0.99 else text
        ch = to_hex_char(ch)
    else:
        ch = ' '
    return ch


def _recognize_digits(
        large_img: np.ndarray,
        horizontal_line_list: list[tuple[int, int]],
        vertical_line_list: list[tuple[int, int]]
) -> list[list[str]]:
    result = [_recognize_text(large_img, x, y, w, h) for y, h in vertical_line_list for x, w in horizontal_line_list]
    return result


def _get_level_str_from_image(large_img: np.ndarray) -> str:
    large_img2 = cv2.cvtColor(large_img, cv2.COLOR_BGR2RGB)
    horizontal_line_results = analyze_horizontal_line(large_img, y_coord=210, start_x=0, end_x=1180)
    processed_horizontal_lines = process_pixel_long_results(horizontal_line_results, is_horizontal=True)
    vertical_line_results = analyze_vertical_line(large_img, x_coord=10, start_y=200, end_y=1380)
    processed_vertical_lines = process_pixel_long_results(vertical_line_results, is_horizontal=False)
    matrix = _recognize_digits(large_img2, processed_horizontal_lines, processed_vertical_lines)
    level_str = '\n'.join([''.join(row) + '`' for row in matrix])
    return level_str


get_levels_str_from_puzzle(
    "Sentinels",
    1,
    54,
    _get_level_str_from_image,
)
