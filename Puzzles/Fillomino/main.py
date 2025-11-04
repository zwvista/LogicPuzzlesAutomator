from typing import Self, override

from Puzzles.puzzle_analyzer import PuzzleAnalyzer, get_level_str_from_matrix, to_base_36


# Games 2 Puzzle Set 4
class _Analyzer(PuzzleAnalyzer):

    def __init__(self: Self):
        super().__init__(
            145,
            [(1, 5), (4, 6), (21, 7), (36, 8), (50, 9), (60, 10), (74, 11), (115, 12)]
        )

    @override
    def get_level_str_from_image(self: Self) -> str:
        horizontal_lines, vertical_lines = self.get_grid_lines_by_cell_count(self.cell_count)
        matrix = self.recognize_digits(horizontal_lines, vertical_lines)
        level_str = get_level_str_from_matrix(matrix, to_base_36)
        return level_str

    @override
    def get_attr_str_from_image(self: Self) -> str:
        output = self.recognize_text(660, 56, 500, 34)
        if not output:
            return ''
        else:
            _, text, _ = output
            return f' GameType="{text.rstrip(" @").replace("AIl", "All") }"'


if __name__ == "__main__":
    analyzer = _Analyzer()
    # analyzer.take_snapshot()
    # analyzer.get_level_board_size_from_puzzle()
    analyzer.get_levels_str_from_puzzle()
