import easyocr
import numpy as np

from Puzzles.common import analyze_horizontal_line, analyze_vertical_line, process_pixel_long_results, \
    get_levels_str_from_puzzle, recognize_digits, recognize_walls

reader = easyocr.Reader(['en'])  # 初始化，只加载英文模型

def _format_digit_matrix(
        matrix: list[list[str]],
        walls: tuple[set[tuple[int, int]], set[tuple[int, int]]]
) -> str:
    lines = []
    rows = len(matrix)
    cols = len(matrix[0])
    row_walls, col_walls = walls
    for r in range(rows + 1):
        line = ''
        for c in range(cols + 1):
            line += ' '
            if c == cols:
                break
            line += '-' if (r, c) in row_walls else ' '
        lines.append(line + '`')
        if r == rows:
            break
        digits = matrix[r]
        line = ''
        for c in range(cols + 1):
            line += '|' if (r, c) in col_walls else ' '
            if c == cols:
                break
            line += digits[c]
        lines.append(line + '`')

    # 合并为多行字符串
    result = '\n'.join(lines)
    return result

def _get_level_str_from_image(large_img: np.ndarray) -> str:
    horizontal_line_results = analyze_horizontal_line(large_img, y_coord=210, start_x=0, end_x=1180)
    processed_horizontal_lines = process_pixel_long_results(horizontal_line_results, is_horizontal=True)
    vertical_line_results = analyze_vertical_line(large_img, x_coord=10, start_y=200, end_y=1380)
    processed_vertical_lines = process_pixel_long_results(vertical_line_results, is_horizontal=False)
    digits_matrix = recognize_digits(reader, large_img, processed_horizontal_lines, processed_vertical_lines)
    walls = recognize_walls(large_img, processed_horizontal_lines, processed_vertical_lines)
    level_str = _format_digit_matrix(digits_matrix, walls)
    return level_str


get_levels_str_from_puzzle("TheOddBrick", 1, 160, _get_level_str_from_image)
