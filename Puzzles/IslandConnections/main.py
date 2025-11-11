from typing import Self, override

import cv2

from Puzzles.puzzle_analyzer import PuzzleAnalyzer, get_level_str_from_matrix


# Games 1 Puzzle Set 16
class _Analyzer(PuzzleAnalyzer):

    def __init__(self: Self):
        super().__init__(
            200,
            [(1, 6), (31, 7), (71, 8), (101, 9), (141, 10)]
        )

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

    def get_scale_for_digit_recognition(self: Self, w: int) -> float:
        return .5 if w > 220 else 1 if w > 180 else 2 if w > 130 else 3 if w > 90 else 5

    def recognize_pattern(
            self: Self,
            horizontal_line_list: list[tuple[int, int]],
            vertical_line_list: list[tuple[int, int]]
    ) -> list[list[str]]:
        result = []
        for row_idx, (y, h) in enumerate(vertical_line_list):
            if row_idx % 2 == 1: continue
            row_result = []
            for col_idx, (x, w) in enumerate(horizontal_line_list):
                if col_idx % 2 == 1: continue
                horizontal_line_results = self.analyze_horizontal_line(y_coord=y + h // 2, start_x=x, end_x=x+w)
                if len(horizontal_line_results) == 1:
                    ch = ' '
                # elif self.recognize_circle(x, y, w, h):
                elif self.large_img_bgr2[y + h // 2, x + 20][0] == 255:
                    ch = 'S'
                else:
                    ch = self.recognize_digit(x, y, w, h) or 'O'
                    ch = 'O' if ch == '6' or ch == '0' else '1' if ch == '01' or ch == '7' else '3' if ch == '63' else ch
                row_result.append(ch)
            result.append(row_result)
        return result

    @override
    def get_level_str_from_image(self: Self) -> str:
        gray = cv2.cvtColor(self.large_img_bgr, cv2.COLOR_BGR2GRAY)
        _, self.large_img_bgr2 = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)
        self.large_img_bgr2 = cv2.cvtColor(self.large_img_bgr2, cv2.COLOR_GRAY2BGR)
        _, self.large_img_bgr = cv2.threshold(gray, 170, 255, cv2.THRESH_BINARY)
        self.large_img_bgr = cv2.cvtColor(self.large_img_bgr, cv2.COLOR_GRAY2BGR)

        horizontal_lines, vertical_lines = self.get_grid_lines_by_cell_count(self.cell_count * 2 - 1)
        matrix = self.recognize_pattern(horizontal_lines, vertical_lines)
        level_str = get_level_str_from_matrix(matrix)
        return level_str


if __name__ == "__main__":
    analyzer = _Analyzer()
    # analyzer.take_snapshot(2)
    # analyzer.get_level_board_size_from_puzzle()
    analyzer.get_levels_str_from_puzzle(141)
