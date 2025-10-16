from typing import Self, override

from Puzzles.puzzle_analyzer import PuzzleAnalyzer, to_base_36, get_level_str_from_matrix


# Games 1 Puzzle Set 2
class _Analyzer(PuzzleAnalyzer):

    def __init__(self: Self):
        super().__init__(
            52,
            [(1,6), (9,7), (18,8), (25,9), (38,10)]
        )

    @override
    def get_scale_for_digit_recognition(self: Self, w: int) -> float:
        return .5 if w > 220 else 1 if w > 180 else 1.5 if w > 130 else 2.5

    @override
    def get_level_str_from_image(self: Self) -> str:
        horizontal_lines, vertical_lines = self.get_grid_lines_by_cell_count(self.cell_count)
        matrix = self.recognize_digits(horizontal_lines, vertical_lines)
        level_str = get_level_str_from_matrix(matrix, to_base_36)
        return level_str


if __name__ == "__main__":
    analyzer = _Analyzer()
