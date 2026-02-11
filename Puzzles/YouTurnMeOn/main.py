from typing import Self, override

import cv2

from Puzzles.puzzle_analyzer import PuzzleAnalyzer, format_matrix_with_walls


class _Analyzer(PuzzleAnalyzer):

    def __init__(self: Self):
        super().__init__(
            400,
            [(1, 4), (21, 5), (31, 6), (96, 7), (156, 8), (286, 9), (336, 10)]
        )

    @override
    def get_scale_for_digit_recognition(self: Self, w: int) -> float:
        return 4 if w > 220 else 4 if w > 180 else 6 if w > 130 else 8

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
                horizontal_line_results = self.analyze_horizontal_line(y_coord=y+20, start_x=x + 10, end_x=x+w - 10)
                if len(horizontal_line_results) == 1:
                    ch = ' '
                else:
                    ch = self.recognize_digit(x, y, w, h) or ' '
                row_result.append(ch)
            result.append(row_result)
        return result

    @override
    def get_level_str_from_image(self: Self) -> str:
        gray = cv2.cvtColor(self.large_img_bgr, cv2.COLOR_BGR2GRAY)
        _, self.large_img_bgr = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
        self.large_img_bgr = cv2.cvtColor(self.large_img_bgr, cv2.COLOR_GRAY2BGR)

        horizontal_lines, vertical_lines = self.get_grid_lines_by_cell_count(self.cell_count)
        vertical_line_results = self.analyze_vertical_line(1170, 210, 1270)
        if len(vertical_line_results) == 1:
            horizontal_lines, vertical_lines = self.get_grid_lines_by_cell_count(self.cell_count + 1)
            horizontal_lines = horizontal_lines[:-1]

        matrix = self.recognize_digits(horizontal_lines, vertical_lines)
        walls = self.recognize_walls2(horizontal_lines, vertical_lines, 255)
        level_str = format_matrix_with_walls(matrix, walls)
        return level_str


if __name__ == "__main__":
    analyzer = _Analyzer()
    # analyzer.take_snapshot(app_series_no=4)
    # analyzer.get_level_board_size_from_puzzle()
    analyzer.get_levels_str_from_puzzle()
