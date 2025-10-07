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

    def recognize_digits(
            self: Self,
            horizontal_line_list: list[tuple[int, int]],
            vertical_line_list: list[tuple[int, int]]
    ) -> list[list[str]]:
        result = []
        for row_idx, (y, h) in enumerate(vertical_line_list):
            row_result = []
            for col_idx, (x, w) in enumerate(horizontal_line_list):
                horizontal_line_results = self.analyze_horizontal_line(y_coord=y + h // 2, start_x=x + 10, end_x=x+w - 10)
                if len(horizontal_line_results) == 1:
                    ch = ' '
                else:
                    ch = self.recognize_digit(x, y, w, h) or ' '
                    ch = self.to_hex_char(ch)
                row_result.append(ch)
            result.append(row_result)
        return result

    @override
    def get_level_str_from_image(self: Self) -> str:
        cell_length = 1180 // self.cell_count
        processed_horizontal_lines2, processed_vertical_lines2 = self.get_normalized_lines(cell_length)
        matrix = self.recognize_digits(processed_horizontal_lines2, processed_vertical_lines2)
        level_str = '\n'.join([''.join(row) + '`' for row in matrix])
        return level_str


analyzer = Analyzer()
analyzer.get_levels_str_from_puzzle(
    83,
    83
)
