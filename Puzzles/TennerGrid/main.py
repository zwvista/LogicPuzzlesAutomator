from typing import Self, override

from Puzzles.puzzle_analyzer import PuzzleAnalyzer, get_level_str_from_matrix


# Puzzle Set 7
class _Analyzer(PuzzleAnalyzer):

    def __init__(self: Self):
        super().__init__(
            24,
            [(1,4), (8,5), (14,6), (19,7)],
            True
        )

    @override
    def get_level_str_from_image(self: Self) -> str:
        horizontal_lines, vertical_lines = self.get_grid_lines_by_cell_count(10)
        vertical_lines = vertical_lines[:self.cell_count]
        matrix = self.recognize_digits(horizontal_lines, vertical_lines)
        level_str = get_level_str_from_matrix(matrix, lambda s: s.rjust(2))
        return level_str


analyzer = _Analyzer()
analyzer.get_levels_str_from_puzzle()

# 22 problem
