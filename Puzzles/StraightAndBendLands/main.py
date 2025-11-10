from typing import Self, override

import cv2

from Puzzles.puzzle_analyzer import PuzzleAnalyzer, format_matrix_with_walls, get_template_img_4channel_list


# Games 2 Puzzle Set 2
class _Analyzer(PuzzleAnalyzer):

    TREE_PATH = '../../images/tree.png'
    HOUSE_PATH = '../../images/lodge.png'
    template_img_4channel_list = get_template_img_4channel_list(TREE_PATH, HOUSE_PATH)

    def __init__(self: Self):
        super().__init__(
            400,
            [(1, 5), (6, 6), (31, 7), (71, 8), (131, 9), (211, 10), (311, 11)]
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
                index = self.get_template_index_by_diff_in_region(
                    template_img_4channel_list=self.template_img_4channel_list,
                    top_left_coord=(x, y),
                    size=(w, h),
                )
                ch = ' ' if index == -1 else 'TO'[index]
                row_result.append(ch)
            result.append(row_result)
        return result

    @override
    def get_level_str_from_image(self: Self) -> str:
        horizontal_lines, vertical_lines = self.get_grid_lines_by_cell_count(self.cell_count)
        matrix = self.recognize_template(horizontal_lines, vertical_lines)

        gray = cv2.cvtColor(self.large_img_bgr, cv2.COLOR_BGR2GRAY)
        _, self.large_img_bgr = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)
        self.large_img_bgr = cv2.cvtColor(self.large_img_bgr, cv2.COLOR_GRAY2BGR)

        walls = self.recognize_walls2(horizontal_lines, vertical_lines, 255)
        level_str = format_matrix_with_walls(matrix, walls)
        return level_str


if __name__ == "__main__":
    analyzer = _Analyzer()
    # analyzer.take_snapshot(app_series_no=4)
    # analyzer.get_level_board_size_from_puzzle()
    analyzer.get_levels_str_from_puzzle()
