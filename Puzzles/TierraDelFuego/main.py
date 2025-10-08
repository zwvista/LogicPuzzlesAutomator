from typing import Self, override

import cv2
import numpy as np

from Puzzles.puzzle_analyzer import PuzzleAnalyzer


class Analyzer(PuzzleAnalyzer):

    def __init__(self: Self):
        super().__init__(
            82
            [(1,5), (4,6), (13,7), (23,8), (35,9), (47,10), (59,11), (71,12)],
            True
        )


    def recognize_characters(
            self: Self,
            horizontal_line_list: list[tuple[int, int]],
            vertical_line_list: list[tuple[int, int]],
            cell_length: int,
    ) -> list[list[str]]:
        def get_roi_large(roi: np.ndarray) -> np.ndarray:
            gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
            _, img_result = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)
            scale = .1 * self.cell_count
            roi_large = cv2.resize(img_result, None, fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)
            return roi_large

        result = []
        for row_idx, (y, h) in enumerate(vertical_line_list):
            row_result = []
            for col_idx, (x, w) in enumerate(horizontal_line_list):
                horizontal_line_results = self.analyze_horizontal_line(y_coord=y + h // 2, start_x=x, end_x=x+w)
                if next((s for s in horizontal_line_results if s.color == (255, 255, 255)), None) is None:
                    ch = ' '
                else:
                    output = self.recognize_text(x, y, w, h, get_roi_large=get_roi_large)
                    if output:
                        _, ch, prob = output
                        ch = 'G' if ch == '6' else ch
                    else:
                        ch = 'I'
                row_result.append(ch)
            result.append(row_result)
        return result


    @override
    def get_level_str_from_image(self: Self) -> str:
        horizontal_line_results = self.analyze_horizontal_line(y_coord=210, start_x=0, end_x=1180)
        processed_horizontal_lines = self.process_pixel_long_results(horizontal_line_results, is_horizontal=True)
        cell_length = max(processed_horizontal_lines, key=lambda x: x[1])[1]
        processed_horizontal_lines2, processed_vertical_lines2 = self.get_normalized_lines(cell_length)
        matrix = self.recognize_characters(processed_horizontal_lines2, processed_vertical_lines2, cell_length)
        level_str = '\n'.join([''.join(row) + '`' for row in matrix])
        return level_str


analyzer = Analyzer()
analyzer.get_levels_str_from_puzzle(
    65,65
    # 1,
    # 82,
)
