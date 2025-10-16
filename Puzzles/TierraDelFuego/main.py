from typing import Self, override

import cv2
import numpy as np

from Puzzles.puzzle_analyzer import PuzzleAnalyzer, get_level_str_from_matrix


# Games 1 Puzzle Set 11
class _Analyzer(PuzzleAnalyzer):

    def __init__(self: Self):
        super().__init__(
            82
            [(1,5), (4,6), (13,7), (23,8), (35,9), (47,10), (59,11), (71,12)]
        )


    def recognize_letters(
            self: Self,
            horizontal_line_list: list[tuple[int, int]],
            vertical_line_list: list[tuple[int, int]],
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
        horizontal_lines, vertical_lines = self.get_grid_lines_by_cell_count(self.cell_count)
        matrix = self.recognize_letters(horizontal_lines, vertical_lines)
        level_str = get_level_str_from_matrix(matrix)
        return level_str


analyzer = _Analyzer()
analyzer.get_levels_str_from_puzzle(
    65,65
    # 1,
    # 82,
)
