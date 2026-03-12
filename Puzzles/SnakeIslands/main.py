from typing import Self, override

from Puzzles.puzzle_analyzer import PuzzleAnalyzer, to_base_36, get_level_str_from_matrix


class _Analyzer(PuzzleAnalyzer):

    def __init__(self: Self):
        super().__init__(
            300,
            [(1, 5), (11, 6), (41, 7), (86, 8), (131, 9), (181, 10), (241, 11)]
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
                horizontal_line_results = self.analyze_horizontal_line(y_coord=y + h // 2, start_x=x + 10, end_x=x+w - 10)
                horizontal_line_results2 = self.analyze_horizontal_line(y_coord=y + 20, start_x=x + 10, end_x=x+w - 10)
                if len(horizontal_line_results) == 1:
                    ch = ' '
                elif len(horizontal_line_results2) != 1:
                    ch = 'S'
                else:
                    ch = self.recognize_digit(x, y, w, h) or ' '
                row_result.append(ch)
            result.append(row_result)
        return result

    @override
    def get_level_str_from_image(self: Self) -> str:
        horizontal_lines, vertical_lines = self.get_grid_lines_by_cell_count(self.cell_count)
        matrix = self.recognize_digits(horizontal_lines, vertical_lines)
        level_str = get_level_str_from_matrix(matrix, to_base_36)
        return level_str


if __name__ == "__main__":
    analyzer = _Analyzer()
    # analyzer.take_snapshot(app_series_no=3)
    # analyzer.get_level_board_size_from_puzzle()
    analyzer.get_levels_str_from_puzzle()
