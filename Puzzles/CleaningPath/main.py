from typing import Self, override

from Puzzles.puzzle_analyzer import PuzzleAnalyzer, format_matrix_with_walls


# Games 1 Puzzle Set 2
class _Analyzer(PuzzleAnalyzer):

    def __init__(self: Self):
        super().__init__(
            300,
            [(1, 4), (11, 5), (21, 6), (51, 7), (71, 8), (131, 9), (161, 10), (231, 11)]
        )

    @override
    def get_level_str_from_image(self: Self) -> str:
        horizontal_lines, vertical_lines = self.get_grid_lines_by_cell_count(self.cell_count)
        horizontal_line_results = self.analyze_horizontal_line(1370, 20, 1170)
        if len(horizontal_line_results) == 1:
            vertical_lines = vertical_lines[:-1]
        matrix = [[' ' for i in range(len(horizontal_lines))] for j in range(len(vertical_lines))]
        walls = self.recognize_walls2(horizontal_lines, vertical_lines, 0)
        level_str = format_matrix_with_walls(matrix, walls)
        return level_str


if __name__ == "__main__":
    analyzer = _Analyzer()
    # analyzer.take_snapshot(3)
    # analyzer.get_level_board_size_from_puzzle()
    analyzer.get_levels_str_from_puzzle()