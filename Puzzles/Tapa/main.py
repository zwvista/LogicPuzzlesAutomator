import cv2
import easyocr
import numpy as np

from Puzzles.common import analyze_horizontal_line, analyze_vertical_line, process_pixel_long_results, \
    get_levels_str_from_puzzle, recognize_digits, recognize_walls, recognize_text

reader = easyocr.Reader(['en'])  # 初始化，只加载英文模型


def _recognize_text(large_img: np.ndarray, x: int, y: int, w: int, h: int) -> str | None:
    roi = large_img[y:y + h, x:x + w]
    roi_large = cv2.resize(roi, None, fx=4, fy=4, interpolation=cv2.INTER_CUBIC)
    output = reader.readtext(roi_large)
    if output:
        output = [('2' if text == "22" else '?' if text == '2' and prob < 0.99 else text)  for _, text, prob in output]
    output_str = ''.join(output) if output else ''
    return f"{output_str:4}"


def _recognize_digits(
        large_img: np.ndarray,
        horizontal_line_list: list[tuple[int, int]],
        vertical_line_list: list[tuple[int, int]]
) -> list[list[str]]:
    result = []
    for row_idx, (y, h) in enumerate(vertical_line_list):
        row_result = []
        for col_idx, (x, w) in enumerate(horizontal_line_list):
            ch = _recognize_text(large_img, x, y, w, h) or [' ']
            row_result.append(ch)
        result.append(row_result)
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


def _get_attr_str_from_image(large_img: np.ndarray) -> str:
    text = recognize_text(reader, large_img, 660, 56, 500, 34)
    return f' GameType="{text}"' if text else ''


get_levels_str_from_puzzle(
    "Tapa",
    44,
    67,
    _get_level_str_from_image,
    _get_attr_str_from_image,
)
