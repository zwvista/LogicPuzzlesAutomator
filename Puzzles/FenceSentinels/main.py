from typing import Self, override

from Puzzles.puzzle_analyzer import PuzzleAnalyzer, get_level_str_from_matrix, to_hex_char


# Puzzle Set 12
class _Analyzer(PuzzleAnalyzer):

    def __init__(self: Self):
        super().__init__(
            84,
            [(1,5), (3,6), (13,7), (21,8), (29,9), (37,10), (53,11), (69,12)],
            True
        )

    @override
    def get_level_str_from_image(self: Self) -> str:
        horizontal_lines, vertical_lines = self.get_grid_lines_by_cell_count(self.cell_count)
        matrix = self.recognize_digits(horizontal_lines, vertical_lines)
        level_str = get_level_str_from_matrix(matrix, to_hex_char)
        return level_str

    @override
    def get_attr_str_from_image(self: Self) -> str:
        output = self.recognize_text(660, 56, 500, 34)
        return f' InsideOutside="1"' if output else ''


analyzer = _Analyzer()
analyzer.get_levels_str_from_puzzle()
