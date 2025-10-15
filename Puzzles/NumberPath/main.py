from typing import Self, override

from Puzzles.puzzle_analyzer import PuzzleAnalyzer, get_level_str_from_matrix


# Games 1 Puzzle Set 15
class _Analyzer(PuzzleAnalyzer):

    def __init__(self: Self):
        super().__init__(
            260,
            [(1,4), (11,5), (31,6), (61,7), (96,8), (151,9), (211,10)],
            True
        )

    @override
    def get_scale_for_digit_recognition(self: Self, w: int) -> float:
        return 1 if w > 220 else 1 if w > 180 else 1.5 if w > 130 else 2.5

    @override
    def get_level_str_from_image(self: Self) -> str:
        horizontal_lines, vertical_lines = self.get_grid_lines_by_cell_count(self.cell_count)
        matrix = self.recognize_digits(horizontal_lines, vertical_lines)
        level_str = get_level_str_from_matrix(matrix, lambda s: s.rjust(2))
        return level_str


analyzer = _Analyzer()
# analyzer.take_snapshot()
analyzer.get_levels_str_from_puzzle()
