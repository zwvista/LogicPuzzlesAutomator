import os

import cv2
import easyocr
import numpy as np

from Puzzles.common import analyze_horizontal_line, process_pixel_long_results, \
    level_node_string, get_template_index_by_diff_in_region, recognize_grid_lines, normalize_lines

CUBE_PATH = '../../images/128/128_icecube.png'
HOLE_PATH = '../../images/TileContent/ice_hole.png'
template_img_4channel_list = [cv2.imread(path, cv2.IMREAD_UNCHANGED) for path in [CUBE_PATH, HOLE_PATH]]

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
            ch = ' ' if index == -1 else 'BH'[index]
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

def get_level_str_from_image(large_img: np.ndarray) -> str:
    processed_horizontal_lines, processed_vertical_lines = recognize_grid_lines(large_img)
    processed_horizontal_lines2 = normalize_lines(processed_horizontal_lines, 2)
    processed_vertical_lines2 = normalize_lines(processed_vertical_lines, 200)
    template_matrix = recognize_template(large_img, processed_horizontal_lines2, processed_vertical_lines2)
    level_str = format_template_matrix(template_matrix)
    return level_str


def main():
    with open(f"Levels.txt", "w"):
        pass
    level_image_path = os.path.expanduser("~/Documents/Programs/Games/100LG/Levels/NorthPoleFishing/")
    START_LEVEL = 181  # 起始关卡: 从1开始
    END_LEVEL = 200  # 结束关卡号
    for i in range(START_LEVEL, END_LEVEL+1):
        # 图像信息
        image_path = f'{level_image_path}Level_{i:03d}.png'
        print("正在处理图片 " + image_path)
        large_img = cv2.imread(image_path, cv2.IMREAD_COLOR)
        if large_img is None:
            print(f"错误：无法加载图像文件。{image_path}")
            continue
        level_str = get_level_str_from_image(large_img)
        node = level_node_string(i, level_str)
        with open(f"Levels.txt", "a") as text_file:
            text_file.write(node)

# --- 主程序 ---
if __name__ == "__main__":
    main()
