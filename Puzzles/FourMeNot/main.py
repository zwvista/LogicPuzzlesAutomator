import os

from Puzzles.common import analyze_horizontal_line, analyze_vertical_line, process_pixel_long_results, recognize_digits, \
    level_node_string, normalize_lines, recognize_blocks, get_template_index_by_diff_in_region

FLOWER_PATH = '../../images/TileContent/flower_blue.png'
MAX_DIFFERENCE = 0.3
block_color = (170, 170, 170, 255)

def recognize_template(image_path, horizontal_line_list, vertical_line_list):
    result = []
    for row_idx, (y, h) in enumerate(vertical_line_list):
        row_result = []
        for col_idx, (x, w) in enumerate(horizontal_line_list):
            index = get_template_index_by_diff_in_region(
                large_image_path=image_path,
                template_path_list=[FLOWER_PATH],
                top_left_coord=(x, y),
                size=(w, h),
            )
            ch = ' ' if index == -1 else 'F'
            row_result.append(ch)
        result.append(row_result)
    return result

def format_template_matrix(matrix, blocks):
    lines = []
    for row_idx, row in enumerate(matrix):
        line = ''
        for col_idx, col in enumerate(row):
            line += 'B' if col == ' ' and (row_idx, col_idx) in blocks else col
        lines.append(line + '`')

    # 合并为多行字符串
    result = '\n'.join(lines)
    return result

def get_level_str_from_image(image_path: str) -> str:
    horizontal_line_results = analyze_horizontal_line(image_path, y_coord=210, start_x=0, end_x=1180)
    processed_horizontal_lines = process_pixel_long_results(horizontal_line_results, is_horizontal=True)
    processed_horizontal_lines2 = normalize_lines(processed_horizontal_lines, start_position=2)
    vertical_line_results = analyze_vertical_line(image_path, x_coord=10, start_y=200, end_y=1380)
    processed_vertical_lines = process_pixel_long_results(vertical_line_results, is_horizontal=False)
    processed_vertical_lines2 = normalize_lines(processed_vertical_lines, start_position=202)
    template_matrix = recognize_template(image_path, processed_horizontal_lines2, processed_vertical_lines2)
    blocks = recognize_blocks(image_path, processed_horizontal_lines2, processed_vertical_lines2, lambda color: color == block_color)
    level_str = format_template_matrix(template_matrix, blocks)
    return level_str


def main():
    level_image_path = os.path.expanduser("~/Documents/Programs/Games/100LG/Levels/FourMeNot/")
    for i in range(1, 41):
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
