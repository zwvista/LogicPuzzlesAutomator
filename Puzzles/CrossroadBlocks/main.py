from typing import Self, override

from Puzzles.puzzle_analyzer import PuzzleAnalyzer, get_template_img_4channel_list


class _Analyzer(PuzzleAnalyzer):

    BLACK_UP_PATH = '../../images/triangle_black_up.png'
    BLACK_RIGHT_PATH = '../../images/triangle_black_right.png'
    BLACK_DOWN_PATH = '../../images/triangle_black_down.png'
    BLACK_LEFT_PATH = '../../images/triangle_black_left.png'
    WHITE_UP_PATH = '../../images/triangle_white_up.png'
    WHITE_RIGHT_PATH = '../../images/triangle_white_right.png'
    WHITE_DOWN_PATH = '../../images/triangle_white_down.png'
    WHITE_LEFT_PATH = '../../images/triangle_white_left.png'
    template_img_4channel_list = get_template_img_4channel_list(
        BLACK_UP_PATH, BLACK_RIGHT_PATH, BLACK_DOWN_PATH, BLACK_LEFT_PATH,
        WHITE_UP_PATH, WHITE_RIGHT_PATH, WHITE_DOWN_PATH, WHITE_LEFT_PATH)

    def __init__(self: Self):
        super().__init__(
            300,
            [(1, 5), (21, 6), (41, 7), (111, 8), (151, 9), (211, 10)]
        )

    def recognize_colors(
            self: Self,
            horizontal_line_list: list[tuple[int, int]],
            vertical_line_list: list[tuple[int, int]]
    ) -> list[list[str]]:
        result = []
        for row_idx, (y, h) in enumerate(vertical_line_list):
            row_result = []
            for col_idx, (x, w) in enumerate(horizontal_line_list):
                if sum((1 if abs(int(self.large_img_bgr[y + dy, x + w // 2][0]) - 116) < 5 else 0) for dy in range(4, 8)) > 1:
                    ch = 'B'
                elif self.large_img_bgr[y + 15, x + w // 2][0] == 255:
                    ch = 'W'
                else:
                    ch = ' '
                row_result.append(ch)
            result.append(row_result)
        return result

    def recognize_digits(
            self: Self,
            horizontal_line_list: list[tuple[int, int]],
            vertical_line_list: list[tuple[int, int]]
    ) -> list[list[str]]:
        result = []
        for row_idx, (y, h) in enumerate(vertical_line_list):
            row_result = []
            for col_idx, (x, w) in enumerate(horizontal_line_list):
                horizontal_line_results = self.analyze_horizontal_line(y_coord=y + h // 2, start_x=x + 10, end_x=x+w - 10)
                if len(horizontal_line_results) == 1:
                    ch = ' '
                else:
                    ch1 = self.recognize_digit(x, y, w // 3, h) or ' '
                    ch2 = self.recognize_digit(x, y, w // 2, h) or ' '
                    ch = ch1 if ch2 == ' ' else ch2
                row_result.append(ch)
            result.append(row_result)
        return result

    def recognize_template(
            self: Self,
            horizontal_line_list: list[tuple[int, int]],
            vertical_line_list: list[tuple[int, int]]
    ) -> list[list[str]]:
        result = []
        for row_idx, (y, h) in enumerate(vertical_line_list):
            row_result = []
            for col_idx, (x, w) in enumerate(horizontal_line_list):
                index = self.get_template_index_by_diff_in_region(
                    template_img_4channel_list=self.template_img_4channel_list,
                    top_left_coord=(x + w // 3, y),
                    size=(w - w // 3, h),
                )
                ch = ' ' if index == -1 else '^>v<^>v<'[index]
                row_result.append(ch)
            result.append(row_result)
        return result

    @staticmethod
    def format_matrix_with_digits(
            matrix: list[list[str]],
            matrix2: list[list[str]],
            matrix3: list[list[str]]
    ) -> str:
        rows, cols = len(matrix), len(matrix[0])
        lines = []
        for r in range(rows):
            line = []
            colors = matrix[r]
            digits = matrix2[r]
            arrows = matrix3[r]
            for c in range(cols):
                c, d, a = colors[c], digits[c], arrows[c]
                if len(d) == 2:
                    d = d[0]
                if c == ' ' and d != ' ':
                    c = 'B'
                str = c + d + a
                if str == 'W <':
                    str = 'W  '
                line.append(str)
            lines.append(''.join(line) + '`')
        result = '\n'.join(lines)
        return result

    @override
    def get_level_str_from_image(self: Self) -> str:
        horizontal_lines, vertical_lines = self.get_grid_lines_by_cell_count(self.cell_count)
        matrix = self.recognize_colors(horizontal_lines, vertical_lines)
        matrix2 = self.recognize_digits(horizontal_lines, vertical_lines)
        matrix3 = self.recognize_template(horizontal_lines, vertical_lines)
        level_str = self.format_matrix_with_digits(matrix, matrix2, matrix3)
        return level_str


if __name__ == "__main__":
    analyzer = _Analyzer()
    # analyzer.take_snapshot(app_series_no=3)
    # analyzer.get_level_board_size_from_puzzle()
    analyzer.get_levels_str_from_puzzle()
