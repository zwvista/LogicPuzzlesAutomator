import os

import cv2
import easyocr
import numpy as np

from Puzzles.common import analyze_horizontal_line, process_pixel_long_results, \
    level_node_string, get_template_index_by_diff_in_region, analyze_vertical_line, get_levels_str_from_puzzle, \
    get_normalized_lines

CUBE_PATH = '../../images/128/128_icecube.png'
HOLE_PATH = '../../images/TileContent/ice_hole.png'
path_list = [f'../../images/TileContent/arrow{n}.png' for n in list("89632147")]
template_img_4channel_list = [cv2.imread(path, cv2.IMREAD_UNCHANGED) for path in path_list]

# reader = easyocr.Reader(['en'])  # 初始化，只加载英文模型

def recognize_template(large_img, horizontal_line_list, vertical_line_list):
    result = []
    for row_idx, (y, h) in enumerate(vertical_line_list):
        row_result = []
        for col_idx, (x, w) in enumerate(horizontal_line_list):
            horizontal_line_results = analyze_horizontal_line(large_img, y_coord=y + h // 2, start_x=x, end_x=x+w)
            processed_horizontal_lines = process_pixel_long_results(horizontal_line_results, is_horizontal=True)
            if len(processed_horizontal_lines) == 1:
                index = -1
            else:
                index = get_template_index_by_diff_in_region(
                    large_img=large_img,
                    template_img_4channel_list=template_img_4channel_list,
                    top_left_coord=(x, y),
                    size=(w, h),
                )
            ch = ' ' if index == -1 else str(index)
            row_result.append(ch)
        result.append(row_result)
    return result


def _get_level_str_from_image(large_img: np.ndarray) -> str:
    horizontal_line_results = analyze_horizontal_line(large_img, y_coord=210, start_x=0, end_x=1180)
    processed_horizontal_lines = process_pixel_long_results(horizontal_line_results, is_horizontal=True)
    cell_length = max(processed_horizontal_lines, key=lambda x: x[1])[1]
    processed_horizontal_lines2, processed_vertical_lines2 = get_normalized_lines(cell_length)
    matrix = recognize_template(large_img, processed_horizontal_lines2, processed_vertical_lines2)
    level_str = '\n'.join([''.join(row) + '`' for row in matrix])
    return level_str


def _get_attr_str_from_image(large_img: np.ndarray, level_str: str) -> str:
    return ' PlantsInEachArea="2"' if len(level_str.split('\n')) >= 9 else ''


get_levels_str_from_puzzle(
    "BotanicalPark",
    1,
    24,
    _get_level_str_from_image,
    _get_attr_str_from_image,
)
