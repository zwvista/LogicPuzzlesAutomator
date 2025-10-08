from typing import Self, override

from Puzzles.puzzle_analyzer import PuzzleAnalyzer

class Analyzer(PuzzleAnalyzer):

    def __init__(self: Self):
        super().__init__(
            16,
            [(1,4), (4,6), (7,8), (13,9), (15,10)],
            True
        )

    @override
    def get_scale_for_digit_recognition(
            self: Self,
            w: int
    ) -> float:
        return .75 if w > 220 else 1 if w > 180 else 1.5 if w > 130 else 2.5

    @override
    def recognize_digits(
            self: Self,
            horizontal_line_list: list[tuple[int, int]],
            vertical_line_list: list[tuple[int, int]]
    ) -> list[list[str]]:
        result = []
        for row_idx, (y, h) in enumerate(vertical_line_list):
            row_result = []
            for col_idx, (x, w) in enumerate(horizontal_line_list):
                # horizontal_line_results = self.analyze_horizontal_line(y_coord=y + h // 2, start_x=x + 10, end_x=x+w - 10)
                # if len(horizontal_line_results) == 1:
                #     ch = ' ' * 3
                # else:
                ch = f"{self.recognize_digit(x, y, w, h) or ' ':>3}"
                row_result.append(ch)
            result.append(row_result)
        return result

    @override
    def get_level_str_from_image(self: Self) -> str:
        cell_length = 1180 // self.cell_count
        processed_horizontal_lines, processed_vertical_lines = self.get_normalized_lines(cell_length)
        matrix = self.recognize_digits(processed_horizontal_lines, processed_vertical_lines)
        level_str = '\n'.join([''.join(row) + '`' for row in matrix])
        return level_str


analyzer = Analyzer()
analyzer.get_levels_str_from_puzzle()
