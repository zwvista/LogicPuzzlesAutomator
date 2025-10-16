from typing import Self, override

from Puzzles.Tatami.main import format_matrix_with_walls
from Puzzles.puzzle_analyzer import PuzzleAnalyzer


# Games 1 Puzzle Set 14
class _Analyzer(PuzzleAnalyzer):

    def __init__(self: Self):
        super().__init__(
            160,
            [(1,4), (16,5), (36,6), (51,7), (91,8), (131,9)]
        )

    @override
    def get_level_str_from_image(self: Self) -> str:
        horizontal_lines, vertical_lines = self.get_grid_lines_by_cell_count(self.cell_count)
        digits_matrix = self.recognize_digits(horizontal_lines, vertical_lines)
        walls = self.recognize_walls(horizontal_lines, vertical_lines)
        level_str = format_matrix_with_walls(digits_matrix, walls)
        return level_str


if __name__ == "__main__":
    analyzer = _Analyzer()
