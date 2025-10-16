from typing import Self, override

from Puzzles.puzzle_analyzer import PuzzleAnalyzer, get_level_str_from_matrix


# Games 1 Puzzle Set 15
class _Analyzer(PuzzleAnalyzer):

    def __init__(self: Self):
        super().__init__(
            250,
            [(1,4), (4,5), (21,6), (51,7), (91,8), (131,9), (171,10), (211,11)]
        )

    @override
    def get_level_str_from_image(self: Self) -> str:
        horizontal_lines, vertical_lines = self.get_grid_lines_by_cell_count(self.cell_count)
        matrix = self.recognize_digits(horizontal_lines, vertical_lines)
        level_str = get_level_str_from_matrix(matrix)
        return level_str


analyzer = _Analyzer()
# analyzer.take_snapshot()
analyzer.get_levels_str_from_puzzle()
