from typing import Self, override

from Puzzles.puzzle_analyzer import PuzzleAnalyzer, format_matrix_with_walls


# Games 1 Puzzle Set 2
class _Analyzer(PuzzleAnalyzer):

    def __init__(self: Self):
        super().__init__(
            200,
            [(1,6), (32,8), (76,9), (119,10), (152,12)]
        )

    @override
    def get_level_str_from_image(self: Self) -> str:
        cell_length = 1180 // self.cell_count
        processed_horizontal_lines, processed_vertical_lines = self.get_grid_lines_by_cell_count(cell_length)
        digits_matrix = self.recognize_digits(processed_horizontal_lines, processed_vertical_lines)
        walls = self.recognize_walls(processed_horizontal_lines, processed_vertical_lines)
        level_str = format_matrix_with_walls(digits_matrix, walls)
        return level_str


if __name__ == "__main__":
    analyzer = _Analyzer()
