from typing import Self, override

from Puzzles.puzzle_analyzer import PuzzleAnalyzer, get_level_str_from_matrix


# Puzzle Set 14
class _Analyzer(PuzzleAnalyzer):

    def __init__(self: Self):
        super().__init__(
            220,
            [(1,9), (61,10), (141,11)],
            True
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
            is_hint_row = row_idx == len(vertical_line_list) - 1
            for col_idx, (x, w) in enumerate(horizontal_line_list):
                is_hint_col = col_idx == len(horizontal_line_list) - 1
                if is_hint_row or is_hint_col:
                    ch = self.recognize_digit(x, y, w, h) or ' '
                else:
                    ch = ' '
                row_result.append(ch)
            result.append(row_result)
        return result


    @override
    def get_level_str_from_image(self: Self) -> str:
        horizontal_lines, vertical_lines = self.get_grid_lines_by_cell_count(self.cell_count + 1)
        matrix = self.recognize_digits(horizontal_lines, vertical_lines)
        level_str = get_level_str_from_matrix(matrix)
        return level_str


analyzer = _Analyzer()
analyzer.get_levels_str_from_puzzle()
