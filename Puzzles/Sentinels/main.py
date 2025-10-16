from typing import Self, override

from Puzzles.puzzle_analyzer import PuzzleAnalyzer, get_level_str_from_matrix, to_base_36


# Games 1 Puzzle Set 3
class _Analyzer(PuzzleAnalyzer):

    def __init__(self: Self):
        super().__init__(
            54,
            [(1,4), (2,5), (8,6), (12,7), (54,8)]
        )

    @override
    def get_level_str_from_image(self: Self) -> str:
        horizontal_lines, vertical_lines = self.get_grid_lines_by_cell_count(self.cell_count)
        matrix = self.recognize_digits(horizontal_lines, vertical_lines)
        level_str = get_level_str_from_matrix(matrix, to_base_36)
        return level_str


if __name__ == "__main__":
    analyzer = _Analyzer()
