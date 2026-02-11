from typing import Self, override

from Puzzles.puzzle_analyzer import PuzzleAnalyzer, to_base_36


class _Analyzer(PuzzleAnalyzer):

    def __init__(self: Self):
        super().__init__(
            152,
            [(1, 5), (13, 6), (28, 7), (124, 8), (133, 9), (140, 10), (142, 11)]
        )

    @staticmethod
    def format_matrix_with_walls2(
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
                line.append(to_base_36(digits[c]))
            lines.append(''.join(line) + '`')
        result = '\n'.join(lines)
        return result

    @override
    def get_level_str_from_image(self: Self) -> str:
        horizontal_lines, vertical_lines = self.get_grid_lines_by_cell_count(self.cell_count)
        matrix = self.recognize_digits(horizontal_lines, vertical_lines)
        walls = self.recognize_walls(horizontal_lines, vertical_lines)
        level_str = self.format_matrix_with_walls2(matrix, walls)
        return level_str


if __name__ == "__main__":
    analyzer = _Analyzer()
    # analyzer.take_snapshot()
    # analyzer.get_level_board_size_from_puzzle()
    analyzer.get_levels_str_from_puzzle()
