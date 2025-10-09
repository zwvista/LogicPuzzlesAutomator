from typing import override, Self

from Puzzles.puzzle_analyzer import PuzzleAnalyzer, get_level_str_from_matrix

white = (255, 255, 255)
white2 = (254, 254, 254)

def process_matrix_with_blocks(
        matrix: list[list[str]],
        blocks: set[tuple[int, int]]
) -> None:
    for row_idx, row in enumerate(matrix):
        for col_idx, col in enumerate(row):
            row[col_idx] = 'W' if col == ' ' and (row_idx, col_idx) in blocks else col


# Games 1 Puzzle Set 2
class _Analyzer(PuzzleAnalyzer):

    def __init__(self: Self):
        super().__init__(
            81,
            [(1,5), (16,6), (24,7), (34,8), (42,9), (50,10), (72,11)],
            True
        )

    @override
    def get_level_str_from_image(self: Self) -> str:
        horizontal_lines, vertical_lines = self.get_grid_lines_by_cell_count(self.cell_count)
        matrix = self.recognize_digits(horizontal_lines, vertical_lines)
        blocks = self.recognize_blocks(horizontal_lines, vertical_lines, lambda color: color in [white, white2])
        process_matrix_with_blocks(matrix, blocks)
        level_str = get_level_str_from_matrix(matrix)
        return level_str


analyzer = _Analyzer()
analyzer.get_levels_str_from_puzzle()
