from typing import Self, override

from Puzzles.puzzle_analyzer import PuzzleAnalyzer


class Analyzer(PuzzleAnalyzer):

    def __init__(self: Self):
        super().__init__(
            "Walls",
            111,
            [(1,6), (10,7), (29,8), (39,9), (48,10), (62,8), (72,9), (92,10)],
            True
        )

    @override
    def get_level_str_from_image(self: Self) -> str:
        cell_length = 1180 // self.cell_count
        processed_horizontal_lines2, processed_vertical_lines2 = self.get_normalized_lines(cell_length)
        matrix = self.recognize_digits(processed_horizontal_lines2, processed_vertical_lines2)
        level_str = '\n'.join([''.join(row) + '`' for row in matrix])
        return level_str


analyzer = Analyzer()
analyzer.get_levels_str_from_puzzle()
