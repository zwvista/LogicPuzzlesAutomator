import os

from Puzzles.common import analyze_horizontal_line, analyze_vertical_line, process_pixel_long_results, \
    recognize_digits, level_node_string, recognize_walls


def format_digit_matrix(
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

def get_level_str_from_image(image_path: str) -> str:
    horizontal_line_results = analyze_horizontal_line(image_path, y_coord=210, start_x=0, end_x=1180)
    processed_horizontal_lines = process_pixel_long_results(horizontal_line_results, is_horizontal=True)
    vertical_line_results = analyze_vertical_line(image_path, x_coord=10, start_y=200, end_y=1380)
    processed_vertical_lines = process_pixel_long_results(vertical_line_results, is_horizontal=False)
    digits_matrix = recognize_digits(image_path, processed_horizontal_lines, processed_vertical_lines)
    walls = recognize_walls(image_path, processed_horizontal_lines, processed_vertical_lines)
    level_str = format_digit_matrix(digits_matrix, walls)
    return level_str


def main():
    level_image_path = os.path.expanduser("~/Documents/Programs/Games/100LG/Levels/Gardener/")
    START_LEVEL = 1  # 起始关卡: 从1开始
    END_LEVEL = 35  # 结束关卡号
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
