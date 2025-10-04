import string
from typing import Self, override

import cv2
import numpy as np

from Puzzles.puzzle_analyzer import PuzzleAnalyzer


class Analyzer(PuzzleAnalyzer):

    def __init__(self: Self):
        super().__init__(
            "CastleBailey",
            [(1,4), (6,5), (21,6), (51,7), (81,8), (111,9), (141,10), (171,11)],
            True
        )


    @override
    def recognize_digit(
            self: Self,
            x: int,
            y: int,
            w: int,
            h: int
    ) -> str | None:
        def get_roi_large(roi: np.ndarray) -> np.ndarray:
            scale = .75 * self.cell_count
            roi_large = cv2.resize(roi, None, fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)
            return roi_large

        x = max(0, min(1180 - w, x))
        output = self.recognize_text(x, y, w, h, allowlist=string.digits, get_roi_large=get_roi_large)
        if not output:
            return None
        else:
            _, text, prob = output
            if prob < 0.99:
                text = "2" if text == "22" else "1" if text == "7" or text == "71" or text == "17" else text
            return text


    def recognize_digits(
            self: Self,
            x_list: list[int],
            y_list: list[int],
            cell_length: int,
    ) -> list[list[str]]:
        result = []
        radius = cell_length // 3
        for row_idx, y in enumerate(y_list):
            row_result = []
            for col_idx, x in enumerate(x_list):
                # horizontal_line_results = self.analyze_horizontal_line(y_coord=y -10, start_x=max(0, x - radius - 5), end_x=x - 5)
                # processed_horizontal_lines = self.process_pixel_long_results(horizontal_line_results, is_horizontal=True, threshold=5)
                # if len(processed_horizontal_lines) == 1:
                #     ch = ' '
                # else:
                ch = self.recognize_digit(x - radius, y - radius, radius * 2, radius * 2) or ' '
                row_result.append(ch)
            result.append(row_result)
        return result


    @override
    def get_level_str_from_image(self: Self) -> str:
        processed_horizontal_lines, processed_vertical_lines = self.recognize_grid_lines()
        start_x, start_y = processed_horizontal_lines[0][0], processed_vertical_lines[0][0]
        cell_length = max(processed_horizontal_lines, key=lambda x: x[1])[1]
        x_list = [start_x + i * cell_length for i in range(self.cell_count + 1)]
        y_list = [start_y + i * cell_length for i in range(self.cell_count + 1)]
        matrix = self.recognize_digits(x_list, y_list, cell_length)
        level_str = '\n'.join([''.join(row) + '`' for row in matrix])
        return level_str


analyzer = Analyzer()
analyzer.get_levels_str_from_puzzle(
    # 151,151
    1,
    200,
)
