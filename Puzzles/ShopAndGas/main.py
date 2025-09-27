import os

from Puzzles.common import analyze_horizontal_line, analyze_vertical_line, process_pixel_long_results, \
    level_node_string, normalize_lines, check_template_list_in_region

HOME_PATH = '../../images/TileContent/home.png'
SHOP_PATH = '../../images/TileContent/shoppingcart.png'
GAS_PATH = '../../images/TileContent/gauge.png'

def recognize_template(image_path, line_list, column_list):
    result = []
    for row_idx, (y, h) in enumerate(column_list):
        row_result = []
        for col_idx, (x, w) in enumerate(line_list):
            index = check_template_list_in_region(
                large_image_path=image_path,
                template_path_list=[HOME_PATH, SHOP_PATH, GAS_PATH],
                top_left_coord=(x, y),
                size=(w, h)
            )
            ch = ' ' if index == -1 else 'HSG'[index]
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

def get_level_str_from_image(image_path: str) -> str:
    horizontal_line_results = analyze_horizontal_line(image_path, y_coord=210, start_x=0, end_x=1180)
    processed_horizontal_lines = process_pixel_long_results(horizontal_line_results, is_horizontal=True)
    processed_horizontal_lines2 = normalize_lines(processed_horizontal_lines, start_position=2)
    vertical_line_results = analyze_vertical_line(image_path, x_coord=10, start_y=200, end_y=1380)
    processed_vertical_lines = process_pixel_long_results(vertical_line_results, is_horizontal=False)
    processed_vertical_lines2 = normalize_lines(processed_vertical_lines, start_position=202)
    template_matrix = recognize_template(image_path, processed_horizontal_lines2, processed_vertical_lines2)
    level_str = format_template_matrix(template_matrix)
    return level_str


def main():
    level_image_path = os.path.expanduser("~/Documents/Programs/Games/100LG/Levels/ShopAndGas/")
    START_LEVEL = 1  # 起始关卡: 从1开始
    END_LEVEL = 36  # 结束关卡号
    with open(f"Levels.txt", "w") as text_file:
        for i in range(START_LEVEL, END_LEVEL+1):
            # 图像信息
            image_path = f'{level_image_path}Level_{i:03d}.png'
            print("正在处理图片 " + image_path)
            level_str = get_level_str_from_image(image_path)
            node = level_node_string(i, level_str)
            text_file.write(node)

# --- 主程序 ---
if __name__ == "__main__":
    main()
