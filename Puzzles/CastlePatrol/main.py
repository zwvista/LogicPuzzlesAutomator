import string
from typing import Self, override

import cv2

from Puzzles.puzzle_analyzer import PuzzleAnalyzer, get_level_str_from_matrix, to_base_36


class _Analyzer(PuzzleAnalyzer):

    def __init__(self: Self):
        super().__init__(
            200,
            [(1, 4), (21, 5), (41, 6), (71, 7), (111, 8), (141, 9), (161, 10)]
        )

    @override
    def recognize_digits(
            self: Self,
            horizontal_line_list: list[tuple[int, int]],
            vertical_line_list: list[tuple[int, int]]
    ) -> list[list[str]]:
        gray = cv2.cvtColor(self.large_img_bgr, cv2.COLOR_BGR2GRAY)
        _, img_result = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)

        result = []
        for row_idx, (y, h) in enumerate(vertical_line_list):
            row_result = []
            for col_idx, (x, w) in enumerate(horizontal_line_list):
                horizontal_line_results = self.analyze_horizontal_line(y_coord=y + 15, start_x=x + 15, end_x=x+w - 15)
                horizontal_line_results2 = self.analyze_horizontal_line(y_coord=y + h // 2, start_x=x + 15, end_x=x+w - 15)
                b1, b2 = len(horizontal_line_results) == 1, len(horizontal_line_results2) == 1
                if b1 and b2:
                    text = ' '
                    ch = ' '
                else:
                    roi = img_result[y:y + h, x:x + w]
                    scale = .5 if w > 220 else 1 if w > 180 else 2 if w > 150 else 3 if w > 120 else 4
                    roi_large = cv2.resize(roi, None, fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)
                    output = self.reader.readtext(roi_large, allowlist=string.digits)
                    if not output:
                        text = " "
                    else:
                        _, text, prob = output[0]
                        text = '2' if text == "22" and prob < 0.99 else text
                    ch = '.' if b1 else 'W'
                row_result.append(to_base_36(text) + ch)
            result.append(row_result)
        return result

    @override
    def get_level_str_from_image(self: Self) -> str:
        horizontal_lines, vertical_lines = self.get_grid_lines_by_cell_count(self.cell_count)
        matrix = self.recognize_digits(horizontal_lines, vertical_lines)
        level_str = get_level_str_from_matrix(matrix)
        return level_str


if __name__ == "__main__":
    analyzer = _Analyzer()
    # analyzer.take_snapshot(app_series_no=2)
    # analyzer.get_level_board_size_from_puzzle()
    analyzer.get_levels_str_from_puzzle()
