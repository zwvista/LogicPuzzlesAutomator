from typing import Self, override

from Puzzles.puzzle_analyzer import PuzzleAnalyzer


def format_matrix_with_walls(
        matrix: list[list[str]],
        walls: tuple[set[tuple[int, int]], set[tuple[int, int]]]
) -> str:
    rows, cols = len(matrix), len(matrix[0])
    row_walls, col_walls = walls
    lines = []
    for r in range(rows + 1):
        line = []
        for c in range(cols + 1):
            line.append(' ')
            if c == cols: break
            line.append('-' if (r, c) in row_walls else ' ')
        lines.append(''.join(line) + '`')
        if r == rows: break
        digits = matrix[r]
        line = []
        for c in range(cols + 1):
            line.append('|' if (r, c) in col_walls else ' ')
            if c == cols: break
            line.append(digits[c])
        lines.append(''.join(line) + '`')
    result = '\n'.join(lines)
    return result


# Puzzle Set 2
class _Analyzer(PuzzleAnalyzer):

    def __init__(self: Self):
        super().__init__(
            200,
            [(1,6), (32,8), (76,9), (119,10), (152,12)],
            True
        )

    @override
    def get_level_str_from_image(self: Self) -> str:
        cell_length = 1180 // self.cell_count
        processed_horizontal_lines, processed_vertical_lines = self.get_grid_lines_by_cell_count(cell_length)
        digits_matrix = self.recognize_digits(processed_horizontal_lines, processed_vertical_lines)
        walls = self.recognize_walls(processed_horizontal_lines, processed_vertical_lines)
        level_str = format_matrix_with_walls(digits_matrix, walls)
        return level_str


analyzer = _Analyzer()
analyzer.get_levels_str_from_puzzle()
