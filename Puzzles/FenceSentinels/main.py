from typing import Self, override

import cv2

from Puzzles.puzzle_analyzer import PuzzleAnalyzer


class Analyzer(PuzzleAnalyzer):

    def __init__(self: Self):
        super().__init__("FenceSentinels", True)

    def recognize_digits(
            self: Self,
            horizontal_line_list: list[tuple[int, int]],
            vertical_line_list: list[tuple[int, int]]
    ) -> list[list[str]]:
        result = []
        for row_idx, (y, h) in enumerate(vertical_line_list):
            row_result = []
            for col_idx, (x, w) in enumerate(horizontal_line_list):
                horizontal_line_results = self.analyze_horizontal_line(y_coord=y + h // 2, start_x=x, end_x=x+w)
                processed_horizontal_lines = self.process_pixel_long_results(horizontal_line_results, is_horizontal=True, threshold=5)
                if len(processed_horizontal_lines) == 1:
                    ch = ' '
                else:
                    ch = self.recognize_digit(x, y, w, h) or ' '
                    ch = self.to_hex_char(ch)
                row_result.append(ch)
            result.append(row_result)
        return result


    @override
    def get_level_str_from_image(self: Self) -> str:
        horizontal_line_results = self.analyze_horizontal_line(y_coord=210, start_x=0, end_x=1180)
        processed_horizontal_lines = self.process_pixel_long_results(horizontal_line_results, is_horizontal=True)
        vertical_line_results = self.analyze_vertical_line(x_coord=10, start_y=200, end_y=1380)
        processed_vertical_lines = self.process_pixel_long_results(vertical_line_results, is_horizontal=False)
        matrix = self.recognize_digits(processed_horizontal_lines, processed_vertical_lines)
        level_str = '\n'.join([''.join(row) + '`' for row in matrix])
        return level_str

    @override
    def get_attr_str_from_image(self: Self) -> str:
        output = self.recognize_text(660, 56, 500, 34)
        return f' InsideOutside="1"' if output else ''


analyzer = Analyzer()
analyzer.get_levels_str_from_puzzle(
    29,29
    # 1,
    # 84,
)
