from Puzzles.common import analyze_horizontal_line, analyze_vertical_line, process_pixel_long_results, recognize_digits, \
    level_node_string, recognize_blocks

from PIL import Image

white = (255, 255, 255, 255)
white2 = (254, 254, 254, 255)

def tweak_color(color):
    return white if color == white2 else color

def format_digit_matrix(matrix, blocks):
    lines = []
    for row_idx, row in enumerate(matrix):
        line = ''
        for col_idx, col in enumerate(row):
            line += 'W' if col == ' ' and (row_idx, col_idx) in blocks else col
        lines.append(line + '`')

    # 合并为多行字符串
    result = '\n'.join(lines)
    return result

def get_level_str_from_image(image_path: str) -> str:
    horizontal_line_results = analyze_horizontal_line(image_path, y_coord=210, start_x=0, end_x=1180, tweak=tweak_color)
    processed_horizontal_lines = process_pixel_long_results(horizontal_line_results, is_horizontal=True)
    # print(processed_horizontal_lines)
    # print("\n" + "="*50 + "\n")
    vertical_line_results = analyze_vertical_line(image_path, x_coord=10, start_y=200, end_y=1380, tweak=tweak_color)
    processed_vertical_lines = process_pixel_long_results(vertical_line_results, is_horizontal=False)
    # print(processed_vertical_lines)
    digits_matrix = recognize_digits(image_path, processed_horizontal_lines, processed_vertical_lines)
    # print(digits_matrix)
    blocks = recognize_blocks(image_path, processed_horizontal_lines, processed_vertical_lines, lambda color: tweak_color(color) == white)
    level_str = format_digit_matrix(digits_matrix, blocks)
    return level_str


def main():
    level_image_path = "~/Documents/Programs/Games/100LG/LightenUp/"
    for i in range(42, 82):
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
