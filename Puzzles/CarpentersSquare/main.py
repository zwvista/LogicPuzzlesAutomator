from typing import Self, override

import cv2

from Puzzles.puzzle_analyzer import PuzzleAnalyzer, get_level_str_from_matrix, to_base_36, \
    get_template_img_4channel_list


# Games 2 Puzzle Set 6
class _Analyzer(PuzzleAnalyzer):

    UP_PATH = '../../images/navigate_up.png'
    DOWN_PATH = '../../images/navigate_down.png'
    LEFT_PATH = '../../images/navigate_left.png'
    RIGHT_PATH = '../../images/navigate_right.png'
    template_img_4channel_list = get_template_img_4channel_list(UP_PATH, DOWN_PATH, LEFT_PATH, RIGHT_PATH)

    def __init__(self: Self):
        super().__init__(
            220,
            [(1, 5), (11, 6), (21, 7), (51, 8), (81, 9), (121, 10), (181, 11)]
        )

    def get_scale_for_digit_recognition(self: Self, w: int) -> float:
        return .5 if w > 220 else 1 if w > 180 else 2 if w > 130 else 3

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
                horizontal_line_results = self.analyze_horizontal_line(y_coord=y + 15, start_x=x + 15, end_x=x+w - 15)
                horizontal_line_results2 = self.analyze_horizontal_line(y_coord=y + h // 2, start_x=x + 15, end_x=x+w - 15)
                b1, b2 = len(horizontal_line_results) == 1, len(horizontal_line_results2) == 1
                if b1 and b2:
                    ch = ' '
                else:
                    index = self.get_template_index_by_diff_in_region(
                        template_img_4channel_list=self.template_img_4channel_list,
                        top_left_coord=(x, y),
                        size=(w, h),
                    )
                    if index != -1:
                        ch = '^v<>'[index]
                    elif not b1 and b2:
                        ch = 'O'
                    else:
                        ch = self.recognize_digit(x, y, w, h) or '7'
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
    # analyzer.take_snapshot()
    # analyzer.get_level_board_size_from_puzzle()
    analyzer.get_levels_str_from_puzzle()
