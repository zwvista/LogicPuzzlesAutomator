import cv2
import easyocr
import numpy as np

from Puzzles.common import get_template_index_by_diff_in_region, recognize_text, get_levels_str_from_puzzle, \
    recognize_grid_lines, get_normalized_lines

A1_PATH = '../../images/TileContent/thermometer1A.png'
A2_PATH = '../../images/TileContent/thermometer2A.png'
A3_PATH = '../../images/TileContent/thermometer3A.png'
template_img_4channel_list_3 = [cv2.imread(path, cv2.IMREAD_UNCHANGED) for path in [A1_PATH, A2_PATH, A3_PATH]]

# a = [1,2,3]
# b = [j for i in a for j in [i, i, i]] #[1,1,1,2,2,2,3,3,3]

template_img_4channel_list_12 = [img2 for img in template_img_4channel_list_3 for img2 in [
    cv2.rotate(img, cv2.ROTATE_180),
    cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE),
    img,
    cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE),
]]

reader = easyocr.Reader(['en'])  # 初始化，只加载英文模型

def recognize_template(large_img, horizontal_line_list, vertical_line_list):
    result = []
    for row_idx, (y, h) in enumerate(vertical_line_list):
        row_result = []
        is_hint_row = row_idx == len(vertical_line_list) - 1
        for col_idx, (x, w) in enumerate(horizontal_line_list):
            is_hint_col = col_idx == len(horizontal_line_list) - 1
            if is_hint_row != is_hint_col:
                ch = recognize_text(reader, large_img, x, y, w, h) or ' '
            elif is_hint_row and is_hint_col:
                ch = ' '
            else:
                index = get_template_index_by_diff_in_region(
                    large_img=large_img,
                    template_img_4channel_list=template_img_4channel_list_12,
                    top_left_coord=(x, y),
                    size=(w, h),
                )
                ch = ' ' if index == -1 else '^>v<++++oooo'[index]
            row_result.append(ch)
        result.append(row_result)
    return result

def format_template_matrix(matrix):
    lines = []
    for row_idx, row in enumerate(matrix):
        line = ''.join(row)
        lines.append(line + '`')

    # 合并为多行字符串
    result = '\n'.join(lines)
    return result

def _get_level_str_from_image(large_img: np.ndarray) -> str:
    processed_horizontal_lines, processed_vertical_lines = recognize_grid_lines(large_img)
    cell_length = max(processed_horizontal_lines, key=lambda x: x[1])[1]
    processed_horizontal_lines2, processed_vertical_lines2 = get_normalized_lines(cell_length)
    template_matrix = recognize_template(large_img, processed_horizontal_lines2, processed_vertical_lines2)
    level_str = format_template_matrix(template_matrix)
    return level_str


get_levels_str_from_puzzle(
    "Thermometers",
    1,
    100,
    _get_level_str_from_image
)
