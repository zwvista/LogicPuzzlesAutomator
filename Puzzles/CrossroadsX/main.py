from typing import Self, override

import cv2

from Puzzles.puzzle_analyzer import PuzzleAnalyzer, format_matrix_with_walls


class _Analyzer(PuzzleAnalyzer):

    def __init__(self: Self):
        super().__init__(
            300,
            [(1, 4), (11, 5), (51, 6), (81, 7), (141, 8), (171, 9), (201, 10), (291, 11)]
        )

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
                horizontal_line_results = self.analyze_horizontal_line(y_coord=y + h // 2, start_x=x + 10, end_x=x+w - 10)
                if len(horizontal_line_results) == 1:
                    ch = ' '
                else:
                    ch = self.recognize_digit(x, y, w, h) or '7'
                row_result.append(ch)
            result.append(row_result)
        return result

    @override
    def get_level_str_from_image(self: Self) -> str:
        horizontal_lines, vertical_lines = self.get_grid_lines_by_cell_count(self.cell_count)
        walls = self.recognize_walls(horizontal_lines, vertical_lines)

        gray = cv2.cvtColor(self.large_img_bgr, cv2.COLOR_BGR2GRAY)
        _, self.large_img_bgr = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)
        self.large_img_bgr = cv2.cvtColor(self.large_img_bgr, cv2.COLOR_GRAY2BGR)

        matrix = self.recognize_digits(horizontal_lines, vertical_lines)
        level_str = format_matrix_with_walls(matrix, walls)
        return level_str

    @override
    def get_attr_str_from_image(self: Self) -> str:
        text = self.recognize_text(840, 56, 320, 34)
        if not text:
            return ''
        return ' sum="15"' if text[1] == 'XV' else ' sum="20"' if text[1] == 'XX Twenty' else ''


if __name__ == "__main__":
    analyzer = _Analyzer()
    # analyzer.take_snapshot(app_series_no=3)
    # analyzer.get_level_board_size_from_puzzle()
    analyzer.get_levels_str_from_puzzle()
