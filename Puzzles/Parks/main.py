from typing import Self, override

from Puzzles.puzzle_analyzer import PuzzleAnalyzer


class ParksBaseAnalyzer(PuzzleAnalyzer):

    def __init__(
            self: Self,
            level_count: int,
            level_to_cell_count: list[tuple[int, int]],
            puzzle_name: str | None = None,
    ):
        super().__init__(level_count, level_to_cell_count, False, puzzle_name)


    def get_combined_pixel_colors(
            self: Self,
            horizontal_line_results: list[tuple[int, int]],
            vertical_line_results: list[tuple[int, int]],
            offset_x:int = 10,
            offset_y:int = 10
    ) -> list[list[tuple[int, int, int]]] | None:
        """
        根据行和列的分析结果，结合偏移量，提取原始图像中指定位置的像素颜色。

        参数:
        image_path (str): 图像文件的路径。
        horizontal_line_results (list): process_pixel_long_results 函数返回的列表，格式为 [(x, count), ...]。
        vertical_line_results (list): process_pixel_long_results 函数返回的列表，格式为 [(y, count), ...]。
        offset_x (int): X方向的偏移量，默认为10。
        offset_y (int): Y方向的偏移量，默认为10。

        返回:
        list: 一个二维列表，其中包含所有组合坐标点的像素颜色。
              如果发生错误，返回 None。
        """
        height, width, _ = self.large_img_bgr.shape

        # 提取所有经过偏移的 X 和 Y 坐标
        x_coords = [item[0] + offset_x for item in horizontal_line_results]
        y_coords = [item[0] + offset_y for item in vertical_line_results]

        # 检查所有计算出的坐标是否在图像尺寸内
        if not all(0 <= x < width for x in x_coords) or not all(0 <= y < height for y in y_coords):
            print(f"错误：计算出的坐标超出了图像尺寸 ({width}x{height})。")
            print(f"计算出的X坐标: {x_coords}")
            print(f"计算出的Y坐标: {y_coords}")
            return None

        # 创建二维数组来存储颜色结果
        color_matrix = []

        for y in y_coords:
            row_colors = []
            for x in x_coords:
                # 获取指定坐标的像素颜色
                b, g, r = self.large_img_bgr[y, x]
                row_colors.append((int(b), int(g), int(r)))
            color_matrix.append(row_colors)

        return color_matrix

    @staticmethod
    def compress_colors_to_codes(color_matrix: list[list[tuple[int, int, int]]]) -> list[list[int]]:
        """
        将二维颜色数组中的颜色替换为数字代码。
        第一种出现的颜色记作0，第二种记作1，以此类推。

        参数:
        color_matrix (list): 由 get_combined_pixel_colors 函数返回的二维颜色数组。

        返回:
        list: 一个二维列表，其中包含对应颜色的数字代码。
        """
        if not color_matrix:
            return []

        # 使用字典存储颜色到数字的映射
        color_to_code = {}
        next_code = 0

        # 创建新的二维数组来存储数字代码
        coded_matrix = []

        for row in color_matrix:
            coded_row = []
            for color in row:
                # 如果颜色不在字典中，分配一个新的代码
                if color not in color_to_code:
                    color_to_code[color] = next_code
                    next_code += 1

                # 将颜色代码添加到行中
                coded_row.append(color_to_code[color])
            coded_matrix.append(coded_row)

        return coded_matrix

    @staticmethod
    def create_grid_string(coded_matrix: list[list[int]]) -> str:
        """
        根据颜色数字矩阵生成一个代表网格布局的多行字符串。

        参数:
        coded_matrix (list): 由 compress_colors_to_codes 返回的二维数字矩阵。

        返回:
        str: 一个表示网格布局的多行字符串。
        """
        if not coded_matrix or not coded_matrix[0]:
            return ""

        m = len(coded_matrix)
        n = len(coded_matrix[0])

        output_lines = []

        # 遍历字符串网格的每一行
        for r2 in range(2 * m + 1):
            line_chars = []
            # 遍历字符串网格的每一列
            for c2 in range(2 * n + 2):

                # 规则 1：一行的最后一个字符
                if c2 == 2 * n + 1:
                    line_chars.append('`')
                    continue

                # 规则 2：网格线的交点或单元格中心
                if (r2 % 2 == 0 and c2 % 2 == 0) or (r2 % 2 != 0 and c2 % 2 != 0):
                    line_chars.append(' ')
                    continue

                # 规则 3：最上或最下边界的水平线
                if (r2 == 0 or r2 == 2 * m) and c2 % 2 != 0:
                    line_chars.append('-')
                    continue

                # 规则 4：最左或最右边界的垂直线
                if (c2 == 0 or c2 == 2 * n) and r2 % 2 != 0:
                    line_chars.append('|')
                    continue

                # 规则 5：内部水平线
                if r2 % 2 == 0 and c2 % 2 != 0:
                    r1 = r2 // 2
                    c1 = (c2 - 1) // 2
                    # 比较相邻单元格的数字
                    if coded_matrix[r1 - 1][c1] == coded_matrix[r1][c1]:
                        line_chars.append(' ')
                    else:
                        line_chars.append('-')
                    continue

                # 规则 6：内部垂直线
                if r2 % 2 != 0 and c2 % 2 == 0:
                    r1 = (r2 - 1) // 2
                    c1 = c2 // 2
                    # 比较相邻单元格的数字
                    if coded_matrix[r1][c1 - 1] == coded_matrix[r1][c1]:
                        line_chars.append(' ')
                    else:
                        line_chars.append('|')
                    continue

            output_lines.append("".join(line_chars))

        return "\n".join(output_lines)

    @override
    def get_level_str_from_image(self: Self) -> str:
        # horizontal_line_results = self.analyze_horizontal_line(y_coord=300, start_x=0, end_x=1180)
        # processed_horizontal_lines = process_pixel_long_results(horizontal_line_results, is_horizontal=True)
        # vertical_line_results = self.analyze_vertical_line(x_coord=100, start_y=200, end_y=1380)
        # processed_vertical_lines = process_pixel_long_results(vertical_line_results, is_horizontal=False)
        processed_horizontal_lines2, processed_vertical_lines2 = self.get_grid_lines_by_cell_count(self.cell_count)
        combined_colors = self.get_combined_pixel_colors(processed_horizontal_lines2, processed_vertical_lines2)
        coded_matrix = self.compress_colors_to_codes(combined_colors)
        level_str = self.create_grid_string(coded_matrix)
        return level_str


class _Analyzer(ParksBaseAnalyzer):

    def __init__(self: Self):
        super().__init__(
            41,
            [(1,5), (7,6), (14,7), (15,9), (16,8), (17,9), (26,10), (33,11), (39,12)],
        )

if __name__ == "__main__":
    analyzer = _Analyzer()
    # analyzer.take_snapshot()
    analyzer.get_levels_str_from_puzzle()
