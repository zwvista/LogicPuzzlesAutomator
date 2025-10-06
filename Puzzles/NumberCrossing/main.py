from typing import Self, override

from Puzzles.puzzle_analyzer import PuzzleAnalyzer


class Analyzer(PuzzleAnalyzer):

    def __init__(self: Self):
        super().__init__(
            "NumberCrossing",
            200,
            [(1,5), (6,6), (31,7), (71,8), (101,9), (141,10), (191,11)],
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
            is_hint_row = row_idx == 0 or row_idx == len(vertical_line_list) - 1
            for col_idx, (x, w) in enumerate(horizontal_line_list):
                is_hint_col = col_idx == 0 or col_idx == len(horizontal_line_list) - 1
                if is_hint_row or is_hint_col:
                    ch = f'{self.recognize_digit(x, y, w, h) or ' ':>2}'
                else:
                    ch = ' ' * 2
                row_result.append(ch)
            result.append(row_result)
        return result

    @override
    def get_level_str_from_image(self: Self) -> str:
        cell_length = 1180 // (self.cell_count + 2)
        processed_horizontal_lines2, processed_vertical_lines2 = self.get_normalized_lines(cell_length)
        matrix = self.recognize_digits(processed_horizontal_lines2, processed_vertical_lines2)
        level_str = '\n'.join([''.join(row) + '`' for row in matrix])
        return level_str


analyzer = Analyzer()
analyzer.get_levels_str_from_puzzle(
    # 1,
    # 1
)
