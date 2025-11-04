import string
from typing import Self, override

import cv2

from Puzzles.puzzle_analyzer import PuzzleAnalyzer, get_level_str_from_matrix


# Games 1 Puzzle Set 17
class _Analyzer(PuzzleAnalyzer):

    def __init__(self: Self):
        super().__init__(
            300,
            [(1, 5), (11, 6), (41, 7), (61, 8), (91, 9), (161, 10), (201, 11), (281, 12)]
        )

    @override
    def recognize_digits(
            self: Self,
            horizontal_line_list: list[tuple[int, int]],
            vertical_line_list: list[tuple[int, int]]
    ) -> list[list[str]]:
        gray = cv2.cvtColor(self.large_img_bgr, cv2.COLOR_BGR2GRAY)
        _, img_result = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)

        result = []
        for row_idx, (y, h) in enumerate(vertical_line_list):
            row_result = []
            for col_idx, (x, w) in enumerate(horizontal_line_list):
                horizontal_line_results = self.analyze_horizontal_line(y_coord=y + h // 2, start_x=x, end_x=x+w)
                if len(horizontal_line_results) == 1:
                    text = ' '
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
                row_result.append(text)
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
    # analyzer.take_snapshot(app_series_no=3)
    # analyzer.get_level_board_size_from_puzzle()
    analyzer.get_levels_str_from_puzzle()
