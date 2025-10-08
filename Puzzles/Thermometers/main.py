from typing import Self, override

import cv2

from Puzzles.puzzle_analyzer import PuzzleAnalyzer


class Analyzer(PuzzleAnalyzer):

    A1_PATH = '../../images/TileContent/thermometer1A.png'
    A2_PATH = '../../images/TileContent/thermometer2A.png'
    A3_PATH = '../../images/TileContent/thermometer3A.png'
    template_img_4channel_list_3 = PuzzleAnalyzer.get_template_img_4channel_list([A1_PATH, A2_PATH, A3_PATH])
    template_img_4channel_list_12 = [img2 for img in template_img_4channel_list_3 for img2 in [
        cv2.rotate(img, cv2.ROTATE_180),
        cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE),
        img,
        cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE),
    ]]

    def __init__(self: Self):
        super().__init__(
            100,
            [(1,4), (11,5), (21,6), (31,7), (51,8), (71,9), (86,10)],
            True
        )

    def recognize_template(
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
        cell_length = 1180 // (self.cell_count + 1)
        processed_horizontal_lines, processed_vertical_lines = self.get_normalized_lines(cell_length)
        matrix = self.recognize_template(processed_horizontal_lines, processed_vertical_lines)
        level_str = '\n'.join([''.join(row) + '`' for row in matrix])
        return level_str



analyzer = Analyzer()
analyzer.get_levels_str_from_puzzle(12, 12)

# string of level 12 is not correct