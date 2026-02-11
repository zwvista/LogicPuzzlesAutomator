from typing import Self, override

import cv2

from Puzzles.puzzle_analyzer import PuzzleAnalyzer, get_level_str_from_matrix


class _Analyzer(PuzzleAnalyzer):

    EMPTY_PATH = '../../images/lawn_background.png'
    template_img_4channel_empty = cv2.imread(EMPTY_PATH, cv2.IMREAD_UNCHANGED)

    def __init__(self: Self):
        super().__init__(
            400,
            [(1, 5), (21, 6), (51, 7), (81, 8), (181, 9), (321, 10)]
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
                diff_empty = self.get_template_diff_in_region(self.template_img_4channel_empty, (x + 20, y + 20), (w - 40, h - 40))
                ch = 'O' if diff_empty == 1 else ' '
                # print(diff_empty, ch)
                row_result.append(ch)
            result.append(row_result)
        return result

    @override
    def get_level_str_from_image(self: Self) -> str:
        horizontal_lines, vertical_lines = self.get_grid_lines_by_cell_count(self.cell_count)
        matrix = self.recognize_template(horizontal_lines, vertical_lines)
        level_str = get_level_str_from_matrix(matrix)
        return level_str


if __name__ == "__main__":
    analyzer = _Analyzer()
    # analyzer.take_snapshot(app_series_no=4)
    # analyzer.get_level_board_size_from_puzzle()
    analyzer.get_levels_str_from_puzzle()
