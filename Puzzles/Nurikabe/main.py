from typing import Self, override

from Puzzles.puzzle_analyzer import PuzzleAnalyzer, get_level_str_from_matrix


# Games 1 Puzzle Set 1
class _Analyzer(PuzzleAnalyzer):

    def __init__(self: Self):
        super().__init__(
            47,
            [(1,5), (3,6), (8,7), (11,8), (14,9), (30,10), (34,11), (44,12)]
        )

    @override
    def get_level_str_from_image(self: Self) -> str:
        horizontal_lines, vertical_lines = self.get_grid_lines_by_cell_count(self.cell_count)
        matrix = self.recognize_digits(horizontal_lines, vertical_lines)
        level_str = get_level_str_from_matrix(matrix)
        return level_str


if __name__ == "__main__":
    analyzer = _Analyzer()
