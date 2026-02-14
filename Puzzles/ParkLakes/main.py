from typing import Self, override

import cv2

from Puzzles.puzzle_analyzer import PuzzleAnalyzer, get_level_str_from_matrix, get_template_img_4channel_list


class _Analyzer(PuzzleAnalyzer):

    QM_PATH = '../../images/qm.png'
    template_img_4channel_list = get_template_img_4channel_list(QM_PATH)

    def __init__(self: Self):
        super().__init__(
            200,
            [(1, 5), (6, 6), (31, 7), (66, 8), (86, 9), (111, 10), (160, 11)]
        )

    @override
    def recognize_digits(
            self: Self,
            horizontal_line_list: list[tuple[int, int]],
            vertical_line_list: list[tuple[int, int]]
    ) -> list[list[str]]:
        result = []
        for row_idx, (y, h) in enumerate(vertical_line_list):
            row_result = []
            for col_idx, (x, w) in enumerate(horizontal_line_list):
                horizontal_line_results = self.analyze_horizontal_line(y_coord=y + h // 2, start_x=x + 10, end_x=x+w - 10)
                if len(horizontal_line_results) == 1:
                    text = ' '
                else:
                    index = self.get_template_index_by_diff_in_region(
                        template_img_4channel_list=self.template_img_4channel_list,
                        top_left_coord=(x, y),
                        size=(w, h),
                    )
                    if index != -1:
                        text = '?'
                    else:
                        text = self.recognize_digit(x, y, w, h) or '?'
                row_result.append(text)
            result.append(row_result)
        return result

    @override
    def get_level_str_from_image(self: Self) -> str:
        horizontal_lines, vertical_lines = self.get_grid_lines_by_cell_count(self.cell_count)

        gray = cv2.cvtColor(self.large_img_bgr, cv2.COLOR_BGR2GRAY)
        _, self.large_img_bgr = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
        self.large_img_bgr = cv2.cvtColor(self.large_img_bgr, cv2.COLOR_GRAY2BGR)
        self.large_img_rgb = cv2.cvtColor(self.large_img_bgr, cv2.COLOR_BGR2RGB)
        # cv2.imshow("Grid Intersections", self.large_img_rgb)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

        matrix = self.recognize_digits(horizontal_lines, vertical_lines)
        level_str = get_level_str_from_matrix(matrix, lambda x: x.rjust(2))
        return level_str


if __name__ == "__main__":
    analyzer = _Analyzer()
    # analyzer.take_snapshot()
    # analyzer.get_level_board_size_from_puzzle()
    analyzer.get_levels_str_from_puzzle()
