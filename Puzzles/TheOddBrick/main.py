from typing import Self, override

from Puzzles.puzzle_analyzer import PuzzleAnalyzer


class Analyzer(PuzzleAnalyzer):

    def __init__(self: Self):
        super().__init__(
            160,
            [(1,4), (16,5), (36,6), (51,7), (91,8), (131,9)],
            True
        )

    def format_digit_matrix(
            self: Self,
            matrix: list[list[str]],
            walls: tuple[set[tuple[int, int]], set[tuple[int, int]]]
    ) -> str:
        lines = []
        rows = len(matrix)
        cols = len(matrix[0])
        row_walls, col_walls = walls
        for r in range(rows + 1):
            line = ''
            for c in range(cols + 1):
                line += ' '
                if c == cols:
                    break
                line += '-' if (r, c) in row_walls else ' '
            lines.append(line + '`')
            if r == rows:
                break
            digits = matrix[r]
            line = ''
            for c in range(cols + 1):
                line += '|' if (r, c) in col_walls else ' '
                if c == cols:
                    break
                line += digits[c]
            lines.append(line + '`')
        result = '\n'.join(lines)
        return result

    @override
    def get_level_str_from_image(self: Self) -> str:
        cell_length = 1180 // self.cell_count
        processed_horizontal_lines, processed_vertical_lines = self.get_normalized_lines(cell_length)
        digits_matrix = self.recognize_digits(processed_horizontal_lines, processed_vertical_lines)
        walls = self.recognize_walls(processed_horizontal_lines, processed_vertical_lines)
        level_str = self.format_digit_matrix(digits_matrix, walls)
        return level_str


analyzer = Analyzer()
analyzer.get_levels_str_from_puzzle()
