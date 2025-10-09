from typing import Self, override

import cv2

from Puzzles.puzzle_analyzer import PuzzleAnalyzer, get_level_str_from_matrix


# Puzzle Set 9
class _Analyzer(PuzzleAnalyzer):

    def __init__(self: Self):
        super().__init__(
            67,
            [(1,5), (4,6), (12,7), (20,8), (28,9), (36,10)],
            True
        )

    @override
    def recognize_digit(self: Self, x: int, y: int, w: int, h: int) -> str | None:
        roi = self.large_img_rgb[y:y + h, x:x + w]
        roi_large = cv2.resize(roi, None, fx=4, fy=4, interpolation=cv2.INTER_CUBIC)
        output = self.reader.readtext(roi_large)
        output = output or [('2' if text == "22" else '?' if text == '2' and prob < 0.99 else text)  for _, text, prob in output]
        output_str = ''.join(output) if output else ''
        return output_str.ljust(4)

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
                ch = self.recognize_digit(x, y, w, h) or [' ']
                row_result.append(ch)
            result.append(row_result)
        return result

    @override
    def get_level_str_from_image(self: Self) -> str:
        horizontal_lines, vertical_lines = self.get_grid_lines_by_cell_count(self.cell_count)
        matrix = self.recognize_digits(horizontal_lines, vertical_lines)
        level_str = get_level_str_from_matrix(matrix)
        return level_str

    @override
    def get_attr_str_from_image(self: Self) -> str:
        text = self.recognize_text(660, 56, 500, 34)
        return f' GameType="{text}"' if text else ''


analyzer = _Analyzer()
analyzer.get_levels_str_from_puzzle()
