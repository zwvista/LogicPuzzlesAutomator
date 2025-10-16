from typing import Self, override

from Puzzles.puzzle_analyzer import PuzzleAnalyzer, to_base_36, get_level_str_from_matrix


# Games 1 Puzzle Set 5
class _Analyzer(PuzzleAnalyzer):

    def __init__(self: Self):
        super().__init__(
            200,
            [(1, 5), (11, 6), (41, 7), (71, 8), (101, 9), (141, 10)]
        )

    @override
    def get_level_str_from_image(self: Self) -> str:
        horizontal_lines, vertical_lines = self.get_grid_lines_by_cell_count(self.cell_count)
        matrix = self.recognize_digits(horizontal_lines, vertical_lines)
        level_str = get_level_str_from_matrix(matrix, to_base_36)
        return level_str


if __name__ == "__main__":
    analyzer = _Analyzer()# analyzer.take_snapshot(app_series_no=2)
    # analyzer.get_level_board_size_from_puzzle()
    analyzer.get_levels_str_from_puzzle()
