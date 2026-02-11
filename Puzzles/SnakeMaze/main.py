import string
from typing import Self, override

import cv2

from Puzzles.puzzle_analyzer import PuzzleAnalyzer, get_template_img_4channel_list, get_level_str_from_matrix


class _Analyzer(PuzzleAnalyzer):

    UP_PATH = '../../images/arrow_cyan_up.png'
    RIGHT_PATH = '../../images/arrow_cyan_right.png'
    DOWN_PATH = '../../images/arrow_cyan_down.png'
    LEFT_PATH = '../../images/arrow_cyan_left.png'
    template_img_4channel_list = get_template_img_4channel_list(UP_PATH, RIGHT_PATH, DOWN_PATH, LEFT_PATH)

    def __init__(self: Self):
        super().__init__(
            200,
            [(1, 5), (21, 6), (51, 7), (81, 8), (111, 9), (151, 10)]
        )

    def recognize_template_and_digits(
            self: Self,
            horizontal_line_list: list[tuple[int, int]],
            vertical_line_list: list[tuple[int, int]]
    ) -> list[list[str]]:
        gray = cv2.cvtColor(self.large_img_bgr, cv2.COLOR_BGR2GRAY)
        _, img_result = cv2.threshold(gray, 250, 255, cv2.THRESH_BINARY)

        result = []
        for row_idx, (y, h) in enumerate(vertical_line_list):
            row_result = []
            for col_idx, (x, w) in enumerate(horizontal_line_list):
                horizontal_line_results = self.analyze_horizontal_line(y_coord=y + h // 2, start_x=x + 15, end_x=x+w - 15)
                if len(horizontal_line_results) == 1:
                    s = 'BB' if horizontal_line_results[0].color[0] == 170 else '  '
                else:
                    index = self.get_template_index_by_diff_in_region(
                        template_img_4channel_list=self.template_img_4channel_list,
                        top_left_coord=(x, y),
                        size=(w, h),
                    )
                    s = '^>v<'[index]
                    roi = img_result[y:y + h, x:x + w]
                    scale = 1 if w > 180 else 2 if w > 150 else 3 if w > 120 else 4
                    roi_large = cv2.resize(roi, None, fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)
                    output = self.reader.readtext(roi_large, allowlist=string.digits)
                    if not output:
                        ch = " "
                    else:
                        _, ch, prob = output[0]
                        ch = '2' if ch == "22" and prob < 0.99 else ch
                    s = ch + s
                row_result.append(s)
            result.append(row_result)
        return result

    @override
    def get_level_str_from_image(self: Self) -> str:
        horizontal_lines, vertical_lines = self.get_grid_lines_by_cell_count(self.cell_count)
        matrix = self.recognize_template_and_digits(horizontal_lines, vertical_lines)
        level_str = get_level_str_from_matrix(matrix)
        return level_str


if __name__ == "__main__":
    analyzer = _Analyzer()
    analyzer.take_snapshot(app_series_no=2)
    analyzer.get_level_board_size_from_puzzle()
    # analyzer.get_levels_str_from_puzzle()
