from itertools import chain
from typing import Self, override

import cv2

from Puzzles.puzzle_analyzer import PuzzleAnalyzer, get_template_img_4channel_list, get_level_str_from_matrix


# Games 1 Puzzle Set 14
class _Analyzer(PuzzleAnalyzer):

    A1_PATH = '../../images/thermometer1A.png'
    A2_PATH = '../../images/thermometer2A.png'
    A3_PATH = '../../images/thermometer3A.png'
    template_img_4channel_list_3 = get_template_img_4channel_list(A1_PATH, A2_PATH, A3_PATH)
    template_img_4channel_list_12 = chain.from_iterable([
        cv2.rotate(img, cv2.ROTATE_180),
        cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE),
        img,
        cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE),
    ] for img in template_img_4channel_list_3)

    def __init__(self: Self):
        super().__init__(
            100,
            [(1,4), (11,5), (21,6), (31,7), (51,8), (71,9), (86,10)]
        )

    def recognize_template_and_digits(
            self: Self,
            horizontal_line_list: list[tuple[int, int]],
            vertical_line_list: list[tuple[int, int]]
    ) -> list[list[str]]:
        result = []
        for row_idx, (y, h) in enumerate(vertical_line_list):
            row_result = []
            is_hint_row = row_idx == len(vertical_line_list) - 1
            for col_idx, (x, w) in enumerate(horizontal_line_list):
                is_hint_col = col_idx == len(horizontal_line_list) - 1
                if is_hint_row != is_hint_col:
                    ch = self.recognize_digit(x, y, w, h) or ' '
                elif is_hint_row and is_hint_col:
                    ch = ' '
                else:
                    index = self.get_template_index_by_diff_in_region(
                        template_img_4channel_list=self.template_img_4channel_list_12,
                        top_left_coord=(x, y),
                        size=(w, h),
                    )
                    ch = ' ' if index == -1 else '^>v<++++oooo'[index]
                row_result.append(ch)
            result.append(row_result)
        return result

    @override
    def get_level_str_from_image(self: Self) -> str:
        horizontal_lines, vertical_lines = self.get_grid_lines_by_cell_count(self.cell_count + 1)
        matrix = self.recognize_template_and_digits(horizontal_lines, vertical_lines)
        level_str = get_level_str_from_matrix(matrix)
        return level_str


if __name__ == "__main__":
    analyzer = _Analyzer()
    analyzer.get_levels_str_from_puzzle(12, 12)

# string of level 12 is not correct
