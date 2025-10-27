from typing import Self, override

import cv2

from Puzzles.puzzle_analyzer import PuzzleAnalyzer, to_base_36, get_level_str_from_matrix


# Games 2 Puzzle Set 7
class _Analyzer(PuzzleAnalyzer):

    def __init__(self: Self):
        super().__init__(
            200,
            [(1, 5), (11, 6), (31, 7), (51, 8), (91, 9), (111, 10), (171, 11)]
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

    def recognize_pattern(
            self: Self,
            horizontal_line_list: list[tuple[int, int]],
            vertical_line_list: list[tuple[int, int]]
    ) -> list[list[str]]:
        result = []
        for row_idx, (y, h) in enumerate(vertical_line_list):
            row_result = []
            for col_idx, (x, w) in enumerate(horizontal_line_list):
                horizontal_line_results = self.analyze_horizontal_line(y_coord=y + 10, start_x=x + 10, end_x=x+w - 10)
                if len(horizontal_line_results) == 1:
                    ch = ' '
                # elif self.recognize_circle(x, y, w, h):
                else:
                    b, g, r = self.large_img_bgr[y + h // 2, x + w // 2]
                    ch = 'B' if b == 0 else 'W'
                row_result.append(ch)
            result.append(row_result)
        return result

    @override
    def get_level_str_from_image(self: Self) -> str:
        horizontal_lines, vertical_lines = self.get_grid_lines_by_cell_count(self.cell_count)
        matrix = self.recognize_pattern(horizontal_lines, vertical_lines)
        level_str = get_level_str_from_matrix(matrix, to_base_36)
        return level_str


if __name__ == "__main__":
    analyzer = _Analyzer()
    # analyzer.take_snapshot(app_series_no=2)
    # analyzer.get_level_board_size_from_puzzle()
    analyzer.get_levels_str_from_puzzle()
