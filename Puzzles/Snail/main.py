from typing import Self, override

from Puzzles.puzzle_analyzer import PuzzleAnalyzer, to_base_36, get_level_str_from_matrix


# Games 1 Puzzle Set 14
class _Analyzer(PuzzleAnalyzer):

    def __init__(self: Self):
        super().__init__(
            100,
            [(1,5), (15,6), (26,7), (37,8), (47,9), (57,10), (77,11)]
        )

    @override
    def get_level_str_from_image(self: Self) -> str:
        horizontal_lines, vertical_lines = self.get_grid_lines_by_cell_count(self.cell_count)
        matrix = self.recognize_digits(horizontal_lines, vertical_lines)
        level_str = get_level_str_from_matrix(matrix, to_base_36)
        return level_str


if __name__ == "__main__":
    analyzer = _Analyzer()
    # analyzer.take_snapshot()
    analyzer.get_levels_str_from_puzzle()
