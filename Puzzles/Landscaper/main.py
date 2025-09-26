import os

from Puzzles.common import analyze_horizontal_line, analyze_vertical_line, process_pixel_long_results, recognize_digits, \
    level_node_string, normalize_lines, check_template_in_region_optimized


TREE_PATH = '../../images/TileContent/tree.png'
FLOWER_PATH = '../../images/TileContent/flower_blue.png'
MAX_DIFFERENCE = 0.3

def recognize_trees_flowers(image_path, line_list, column_list):
    result = []
    for row_idx, (y, h) in enumerate(column_list):
        row_result = []
        for col_idx, (x, w) in enumerate(line_list):
            found_tree = check_template_in_region_optimized(
                large_image_path=image_path,
                template_path=TREE_PATH,
                top_left_coord=(x, y),
                size=(w, h),
                max_diff=MAX_DIFFERENCE
            )
            found_flower = check_template_in_region_optimized(
                large_image_path=image_path,
                template_path=FLOWER_PATH,
                top_left_coord=(x, y),
                size=(w, h),
                max_diff=MAX_DIFFERENCE
            )
            ch = 'T' if found_tree else 'F' if found_flower else ' '
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

def get_level_str_from_image(image_path):
    horizontal_line_results = analyze_horizontal_line(image_path, y_coord=210, start_x=0, end_x=1180)
    processed_line_list = process_pixel_long_results(horizontal_line_results, is_horizontal=True)
    processed_line_list2 = normalize_lines(processed_line_list, start_position=2)
    vertical_line_results = analyze_vertical_line(image_path, x_coord=10, start_y=200, end_y=1380)
    processed_column_list = process_pixel_long_results(vertical_line_results, is_horizontal=False)
    processed_column_list2 = normalize_lines(processed_column_list, start_position=202)
    template_matrix = recognize_trees_flowers(image_path, processed_line_list2, processed_column_list2)
    level_str = format_template_matrix(template_matrix)
    return level_str


def main():
    level_image_path = os.path.expanduser("~/Documents/Programs/Games/100LG/Landscaper/")
    for i in range(13, 36):
        # 图像信息
        image_path = f'{level_image_path}Level_{i:03d}.png'
        print("正在处理图片 " + image_path)
        level_str = get_level_str_from_image(image_path)
        node = level_node_string(i, level_str)
        with open(f"Levels.txt", "a") as text_file:
            text_file.write(node)

# --- 主程序 ---
if __name__ == "__main__":
    main()
