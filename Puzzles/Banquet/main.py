import string
from typing import Self, override

import cv2

from Puzzles.puzzle_analyzer import PuzzleAnalyzer, get_level_str_from_matrix, to_base_36, \
    get_template_img_4channel_list


class _Analyzer(PuzzleAnalyzer):

    WOOD_PATH = '../../images/wood1.png'
    WOOD_QM_PATH = '../../images/wood_qm.png'
    template_img_4channel_list = get_template_img_4channel_list(WOOD_PATH, WOOD_QM_PATH)

    def __init__(self: Self):
        super().__init__(
            300,
            [(1, 5), (11, 6), (41, 7), (101, 8), (161, 9), (221, 10)]
        )

    @override
    def recognize_digits(
            self: Self,
            horizontal_line_list: list[tuple[int, int]],
            vertical_line_list: list[tuple[int, int]]
    ) -> list[list[str]]:
        gray = cv2.cvtColor(self.large_img_bgr, cv2.COLOR_BGR2GRAY)
        _, img_result = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)

        result = []
        for row_idx, (y, h) in enumerate(vertical_line_list):
            row_result = []
            for col_idx, (x, w) in enumerate(horizontal_line_list):
                diff_list = [self.get_template_diff_in_region(
                    template_img_4channel=template_img_4channel,
                    top_left_coord=(x, y),
                    size=(w, h),
                ) for template_img_4channel in self.template_img_4channel_list]
                if diff_list[0] > .1:
                    ch = ' '
                elif diff_list[0] < .01:
                    ch = '0'
                elif diff_list[1] < .03:
                    ch = '?'
                else:
                    # print(f'{row_idx=}, {col_idx=}, {diff_list=}')
                    roi = img_result[y:y + h, x:x + w]
                    scale = .1 * self.cell_count
                    roi_large = cv2.resize(roi, None, fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)
                    output = self.reader.readtext(roi_large, allowlist=string.digits)
                    if not output:
                        ch = '7'
                    else:
                        _, ch, prob = output[0]
                        ch = '2' if ch == "22" else ch
                row_result.append(ch)
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
    # analyzer.take_snapshot(app_series_no=3)
    # analyzer.get_level_board_size_from_puzzle()
    analyzer.get_levels_str_from_puzzle(189)
