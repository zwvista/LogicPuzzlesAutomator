import cv2
import numpy as np

from Puzzles.common import analyze_horizontal_line, analyze_vertical_line, process_pixel_long_results, \
    normalize_lines, get_template_index_by_diff_in_region, get_levels_str_from_puzzle

HOME_PATH = '../../images/TileContent/home.png'
SHOP_PATH = '../../images/TileContent/shoppingcart.png'
GAS_PATH = '../../images/TileContent/gauge.png'
template_img_4channel_list = [cv2.imread(path, cv2.IMREAD_UNCHANGED) for path in [HOME_PATH, SHOP_PATH, GAS_PATH]]

def _recognize_template(large_img, horizontal_line_list, vertical_line_list):
    result = []
    for row_idx, (y, h) in enumerate(vertical_line_list):
        row_result = []
        for col_idx, (x, w) in enumerate(horizontal_line_list):
            index = get_template_index_by_diff_in_region(
                large_img=large_img,
                template_img_4channel_list=template_img_4channel_list,
                top_left_coord=(x, y),
                size=(w, h),
            )
            ch = ' ' if index == -1 else 'HSG'[index]
            row_result.append(ch)
        result.append(row_result)
    return result

def _format_template_matrix(matrix):
    lines = []
    for row_idx, row in enumerate(matrix):
        line = ''.join(row)
        lines.append(line + '`')

    # 合并为多行字符串
    result = '\n'.join(lines)
    return result

def _get_level_str_from_image(large_img: np.ndarray) -> str:
    horizontal_line_results = analyze_horizontal_line(large_img, y_coord=210, start_x=0, end_x=1180)
    processed_horizontal_lines = process_pixel_long_results(horizontal_line_results, is_horizontal=True)
    processed_horizontal_lines2 = normalize_lines(processed_horizontal_lines, start_position=2)
    vertical_line_results = analyze_vertical_line(large_img, x_coord=10, start_y=200, end_y=1380)
    processed_vertical_lines = process_pixel_long_results(vertical_line_results, is_horizontal=False)
    processed_vertical_lines2 = normalize_lines(processed_vertical_lines, start_position=202)
    template_matrix = _recognize_template(large_img, processed_horizontal_lines2, processed_vertical_lines2)
    level_str = _format_template_matrix(template_matrix)
    return level_str


get_levels_str_from_puzzle("ShopAndGas", 1, 36, _get_level_str_from_image)
