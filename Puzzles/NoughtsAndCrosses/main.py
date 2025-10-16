from typing import Self, override

import cv2
import numpy as np

from Puzzles.puzzle_analyzer import PuzzleAnalyzer, to_base_36, get_level_str_from_matrix


# Games 1 Puzzle Set 5
class _Analyzer(PuzzleAnalyzer):

    def __init__(self: Self):
        super().__init__(
            300,
            [(1, 4), (4, 5), (81, 6), (151, 7), (211, 8), (261, 9)]
        )

    def recognize_cross(self: Self, x: int, y: int, w: int, h: int) -> bool:
        roi = self.large_img_bgr[y:y + h, x:x + w]
        gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        linesP = cv2.HoughLinesP(
            blur,
            1,
            np.radians(1),
            15,
            minLineLength=w - 5,
            maxLineGap=30
        )
        # for line in linesP:
        #     x1, y1, x2, y2 = line[0]
        #     cv2.line(roi, (x1, y1), (x2, y2), (0, 255, 0), 1)
        # cv2.imshow("roi", roi)
        # cv2.waitKey(0)
        return any(x1 < 20 and h - y1 < 20 and y2 < 20 and w - x2 < 20 for line in linesP for x1, y1, x2, y2 in line)

    def recognize_circle(self: Self, x: int, y: int, w: int, h: int) -> bool:
        roi = self.large_img_bgr[y:y + h, x:x + w]
        gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        maxRadius = w
        minRadius = w // 2 - 10
        circles = cv2.HoughCircles(image=gray,
                                   method=cv2.HOUGH_GRADIENT,
                                   dp=1.2,
                                   minDist=2 * minRadius,
                                   param1=50,
                                   param2=50,
                                   minRadius=minRadius,
                                   maxRadius=maxRadius
                                   )
        return circles is not None

    def recognize_pattern(
            self: Self,
            horizontal_line_list: list[tuple[int, int]],
            vertical_line_list: list[tuple[int, int]]
    ) -> list[list[str]]:
        result = []
        for row_idx, (y, h) in enumerate(vertical_line_list):
            row_result = []
            for col_idx, (x, w) in enumerate(horizontal_line_list):
                horizontal_line_results = self.analyze_horizontal_line(y_coord=y + h // 2, start_x=x, end_x=x+w)
                if len(horizontal_line_results) == 1:
                    ch = ' '
                elif self.recognize_cross(x, y, w, h):
                    ch = 'X'
                elif self.recognize_circle(x, y, w, h):
                    ch = 'O'
                else:
                    ch = self.recognize_digit(x, y, w, h) or ' '
                row_result.append(ch)
            result.append(row_result)
        return result

    @override
    def get_level_str_from_image(self: Self) -> str:
        horizontal_lines, vertical_lines = self.get_grid_lines_by_cell_count(self.cell_count)
        matrix = self.recognize_pattern(horizontal_lines, vertical_lines)
        level_str = get_level_str_from_matrix(matrix, to_base_36)
        return level_str

    @override
    def get_attr_str_from_image(self: Self) -> str:
        result = self.recognize_text(840, 56, 320, 34)
        return f' num="{result[1][2:]}"'


analyzer = _Analyzer()
# analyzer.take_snapshot()
# analyzer.get_level_board_size_from_puzzle()
analyzer.get_levels_str_from_puzzle()
