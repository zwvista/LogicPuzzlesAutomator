import os

from Puzzles.common import analyze_horizontal_line, analyze_vertical_line, process_pixel_long_results, recognize_digits, \
    level_node_string, to_hex_char


def format_digit_matrix(matrix):
    lines = []
    for row_str in matrix:
        line = ''
        for col_str in row_str:
            line += to_hex_char(col_str)
        lines.append(line + '`')
    result = '\n'.join(lines)
    return result


def get_level_str_from_image(image_path):
    horizontal_line_results = analyze_horizontal_line(image_path, y_coord=210, start_x=0, end_x=1180)
    processed_line_list = process_pixel_long_results(horizontal_line_results, is_horizontal=True)
    vertical_line_results = analyze_vertical_line(image_path, x_coord=10, start_y=200, end_y=1380)
    processed_column_list = process_pixel_long_results(vertical_line_results, is_horizontal=False)
    digits_matrix = recognize_digits(image_path, processed_line_list, processed_column_list)
    level_str = format_digit_matrix(digits_matrix)
    return level_str


def main():
    level_image_path = os.path.expanduser("~/Documents/Programs/Games/100LG/Levels/Walls/")
    START_LEVEL = 1  # 起始关卡: 从1开始
    END_LEVEL = 111  # 结束关卡号
    for i in range(START_LEVEL, END_LEVEL+1):
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
