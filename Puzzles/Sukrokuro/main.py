from typing import Self, override

from Puzzles.puzzle_analyzer import PuzzleAnalyzer, get_level_str_from_matrix


class _Analyzer(PuzzleAnalyzer):

    def __init__(self: Self):
        super().__init__(
            200,
            [(1, 11)]
        )

    @override
    def recognize_digits(
            self: Self,
            horizontal_line_list: list[tuple[int, int]],
            vertical_line_list: list[tuple[int, int]]
    ) -> list[list[str]]:
        result = []
        for row_idx, (y, h) in enumerate(vertical_line_list):
            row_result = []
            for col_idx, (x, w) in enumerate(horizontal_line_list):
                if self.large_img_bgr[y + 15, x + w // 3][0] == 0:
                    text = (' .' if 250 <= self.large_img_bgr[y + h, x + w // 2][0] <= 255 else '  ') + \
                           (' .' if 250 <= self.large_img_bgr[y + h // 2, x + w][0] <= 255 else '  ')
                else:
                    horizontal_line_results = self.analyze_horizontal_line(y_coord=y + h // 4 * 3, start_x=x + 10, end_x=x + w // 2 - 10)
                    n1 = '' if len(horizontal_line_results) == 1 else self.recognize_digit(x, y + h // 2, w // 2, h // 2) or '7'
                    horizontal_line_results = self.analyze_horizontal_line(y_coord=y + h // 4, start_x=x + w // 2 + 10, end_x=x + w - 10)
                    n2 = '' if len(horizontal_line_results) == 1 else self.recognize_digit(x + w // 2, y, w // 2, h // 2) or '7'
                    text = n1.zfill(2)[:2] + n2.zfill(2)[:2]
                row_result.append(text)
            result.append(row_result)
        return result

    @override
    def get_level_str_from_image(self: Self) -> str:
        horizontal_lines, vertical_lines = self.get_grid_lines_by_cell_count(self.cell_count)
        matrix = self.recognize_digits(horizontal_lines, vertical_lines)
        level_str = get_level_str_from_matrix(matrix)
        return level_str


if __name__ == "__main__":
    analyzer = _Analyzer()
    # analyzer.take_snapshot(app_series_no=2)
    # analyzer.get_level_board_size_from_puzzle()
    analyzer.get_levels_str_from_puzzle()
