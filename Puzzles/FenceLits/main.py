from typing import Self, override

from Puzzles.puzzle_analyzer import PuzzleAnalyzer, get_level_str_from_matrix


# Games 1 Puzzle Set 12
class _Analyzer(PuzzleAnalyzer):

    def __init__(self: Self):
        super().__init__(
            50,
            [(1,4), (3,6), (11,8), (26,10), (46,12)],
            True
        )

    @override
    def get_level_str_from_image(self: Self) -> str:
        horizontal_lines, vertical_lines = self.get_grid_lines_by_cell_count(self.cell_count)
        matrix = self.recognize__digits(horizontal_lines, vertical_lines)
        level_str = get_level_str_from_matrix(matrix)
        return level_str


analyzer = _Analyzer()
analyzer.get_levels_str_from_puzzle()
