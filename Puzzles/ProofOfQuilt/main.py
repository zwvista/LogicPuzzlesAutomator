from typing import Self, override

from Puzzles.puzzle_analyzer import PuzzleAnalyzer, get_level_str_from_matrix


def process_matrix_with_blocks(
        matrix: list[list[str]],
        blocks: set[tuple[int, int]]
) -> None:
    for row_idx, row in enumerate(matrix):
        for col_idx, col in enumerate(row):
            row[col_idx] = 'W' if col == ' ' and (row_idx, col_idx) in blocks else col

class _Analyzer(PuzzleAnalyzer):

    def __init__(self: Self):
        super().__init__(
            27,
            [(1, 5), (6, 6), (9, 7), (12, 8), (14, 9), (17, 10)]
        )

    @override
    def get_level_str_from_image(self: Self) -> str:
        horizontal_lines, vertical_lines = self.get_grid_lines_by_cell_count(self.cell_count)
        matrix = self.recognize_digits(horizontal_lines, vertical_lines)
        blocks = self.recognize_blocks(horizontal_lines, vertical_lines, lambda color: color[0] == 255)
        process_matrix_with_blocks(matrix, blocks)
        level_str = get_level_str_from_matrix(matrix)
        return level_str


if __name__ == "__main__":
    analyzer = _Analyzer()
    # analyzer.take_snapshot()
    # analyzer.get_level_board_size_from_puzzle()
    analyzer.get_levels_str_from_puzzle()
