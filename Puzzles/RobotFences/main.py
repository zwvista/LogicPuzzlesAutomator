from typing import Self, override

from Puzzles.puzzle_analyzer import PuzzleAnalyzer, format_matrix_with_walls


class _Analyzer(PuzzleAnalyzer):

    def __init__(self: Self):
        super().__init__(
            150,
            [(1, 4), (5, 5), (31, 6), (61, 7), (91, 8), (121, 9)]
        )

    @override
    def get_level_str_from_image(self: Self) -> str:
        horizontal_lines, vertical_lines = self.get_grid_lines_by_cell_count(self.cell_count)
        matrix = self.recognize_digits(horizontal_lines, vertical_lines)
        walls = self.recognize_walls(horizontal_lines, vertical_lines)
        level_str = format_matrix_with_walls(matrix, walls)
        return level_str


if __name__ == "__main__":
    analyzer = _Analyzer()
    # analyzer.take_snapshot()
    # analyzer.get_level_board_size_from_puzzle()
    analyzer.get_levels_str_from_puzzle()
