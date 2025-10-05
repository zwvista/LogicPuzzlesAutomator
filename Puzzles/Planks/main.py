import string
from typing import Self, override

import cv2
import numpy as np

from Puzzles.puzzle_analyzer import PuzzleAnalyzer


class Analyzer(PuzzleAnalyzer):

    A3_PATH = '../../images/TileContent/nail_head.png'
    template_img_4channel_list = PuzzleAnalyzer.get_template_img_4channel_list([A3_PATH])

    def __init__(self: Self):
        super().__init__(
            "Planks",
            [(1,6), (11,7), (31,8), (71,9), (121,10), (181,11)],
            False
        )

    def recognize_template(
            self: Self,
            horizontal_line_list: list[tuple[int, int]],
            vertical_line_list: list[tuple[int, int]]
    ) -> list[list[str]]:
        result = []
        for row_idx, (y, h) in enumerate(vertical_line_list):
            row_result = []
            for col_idx, (x, w) in enumerate(horizontal_line_list):
                horizontal_line_results = self.analyze_horizontal_line(y_coord=y + h // 2, start_x=x, end_x=x+w)
                processed_horizontal_lines = self.process_pixel_long_results(horizontal_line_results, is_horizontal=True, threshold=5)
                if len(processed_horizontal_lines) == 1:
                    ch = ' '
                else:
                    index = self.get_template_index_by_diff_in_region(
                        template_img_4channel_list=self.template_img_4channel_list,
                        top_left_coord=(x, y),
                        size=(w, h),
                    )
                    ch = ' ' if index == -1 else 'N'
                row_result.append(ch)
            result.append(row_result)
        return result

    @override
    def get_level_str_from_image(self: Self) -> str:
        horizontal_line_results = self.analyze_horizontal_line(y_coord=210, start_x=0, end_x=1180)
        processed_horizontal_lines = self.process_pixel_long_results(horizontal_line_results, is_horizontal=True)
        cell_length = max(processed_horizontal_lines, key=lambda x: x[1])[1]
        processed_horizontal_lines2, processed_vertical_lines2 = self.get_normalized_lines(cell_length)
        matrix = self.recognize_template(processed_horizontal_lines2, processed_vertical_lines2)
        level_str = '\n'.join([''.join(row) + '`' for row in matrix])
        return level_str


analyzer = Analyzer()
analyzer.get_levels_str_from_puzzle(
    1,
    250,
)
