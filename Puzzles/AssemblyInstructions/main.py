from typing import Self, override

import cv2
import numpy as np

from Puzzles.puzzle_analyzer import PuzzleAnalyzer, get_level_str_from_matrix


class _Analyzer(PuzzleAnalyzer):

    def __init__(self: Self):
        super().__init__(
            400,
            [(1, 4), (11, 5), (31, 6), (71, 7), (151, 8), (231, 9), (311, 10), (391, 11)]
        )

    def recognize_chars(
            self: Self,
            horizontal_line_list: list[tuple[int, int]],
            vertical_line_list: list[tuple[int, int]]
    ) -> list[list[str]]:
        def get_roi_large(roi: np.ndarray) -> np.ndarray:
            scale = .1 * self.cell_count
            roi_large = cv2.resize(roi, None, fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)
            return roi_large

        result = []
        for row_idx, (y, h) in enumerate(vertical_line_list):
            row_result = []
            for col_idx, (x, w) in enumerate(horizontal_line_list):
                horizontal_line_results = self.analyze_horizontal_line(y_coord=y + h // 2, start_x=x + 20, end_x=x+w - 20)
                if len(horizontal_line_results) == 1:
                    ch = ' '
                else:
                    output = self.recognize_text(x, y, w, h, get_roi_large=get_roi_large)
                    if output:
                        _, ch, prob = output
                        ch = 'G' if ch == "6" else ch
                    else:
                        ch = 'I'
                row_result.append(ch)
            result.append(row_result)
        return result


    @override
    def get_level_str_from_image(self: Self) -> str:
        horizontal_lines, vertical_lines = self.get_grid_lines_by_cell_count(self.cell_count)
        matrix = self.recognize_chars(horizontal_lines, vertical_lines)
        level_str = get_level_str_from_matrix(matrix)
        return level_str


if __name__ == "__main__":
    analyzer = _Analyzer()
    # analyzer.take_snapshot(app_series_no=4)
    # analyzer.get_level_board_size_from_puzzle()
    analyzer.get_levels_str_from_puzzle()
