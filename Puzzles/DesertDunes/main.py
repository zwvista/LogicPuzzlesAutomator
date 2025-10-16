import string
from typing import Self, override

import cv2

from Puzzles.puzzle_analyzer import PuzzleAnalyzer, get_level_str_from_matrix, to_base_36


# Games 1 Puzzle Set 17
class _Analyzer(PuzzleAnalyzer):

    def __init__(self: Self):
        super().__init__(
            200,
            [(1,5), (6,6), (31,7), (76,8), (121,9), (151,10), (191,11)]
        )

    @override
    def recognize_digits(
            self: Self,
            horizontal_line_list: list[tuple[int, int]],
            vertical_line_list: list[tuple[int, int]]
    ) -> list[list[str]]:
        gray = cv2.cvtColor(self.large_img, cv2.COLOR_BGR2GRAY)
        _, img_result = cv2.threshold(gray, 250, 255, cv2.THRESH_BINARY)

        result = []
        for row_idx, (y, h) in enumerate(vertical_line_list):
            row_result = []
            for col_idx, (x, w) in enumerate(horizontal_line_list):
                roi = img_result[y:y + h, x:x + w]
                roi_large = cv2.resize(roi, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
                output = self.reader.readtext(roi_large, allowlist=string.digits)
                if not output:
                    text = " "
                else:
                    _, text, prob = output[0]
                    if text == "22":
                        if prob < 0.99:
                            text = "2"
                row_result.append(text)
            result.append(row_result)
        return result

    @override
    def get_level_str_from_image(self: Self) -> str:
        horizontal_lines, vertical_lines = self.get_grid_lines_by_cell_count(self.cell_count)
        matrix = self.recognize_digits(horizontal_lines, vertical_lines)
        level_str = get_level_str_from_matrix(matrix, to_base_36)
        return level_str


if __name__ == "__main__":
    analyzer = _Analyzer()
