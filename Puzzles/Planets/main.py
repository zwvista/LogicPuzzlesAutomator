from typing import Self, override

from Puzzles.puzzle_analyzer import PuzzleAnalyzer, get_template_img_4channel_list, get_level_str_from_matrix


class _Analyzer(PuzzleAnalyzer):
    P1_PATH = '../../images/planet_all.png'
    P2_PATH = '../../images/planet_down.png'
    P3_PATH = '../../images/planet_down_left.png'
    P4_PATH = '../../images/planet_down_right.png'
    P5_PATH = '../../images/planet_left.png'
    P6_PATH = '../../images/planet_right.png'
    P7_PATH = '../../images/planet_up.png'
    P8_PATH = '../../images/planet_up_left.png'
    P9_PATH = '../../images/planet_up_right.png'
    template_img_4channel_list = get_template_img_4channel_list(P1_PATH, P2_PATH, P3_PATH, P4_PATH, P5_PATH, P6_PATH, P7_PATH, P8_PATH, P9_PATH)

    def __init__(self: Self):
        super().__init__(
            200,
            [(1, 4), (11, 5), (41, 6), (71, 7), (101, 8), (131, 9), (161, 10)]
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
                horizontal_line_results = self.analyze_horizontal_line(y_coord=y + h // 2, start_x=x, end_x=x+w-1)
                if len(horizontal_line_results) == 1:
                    index = -1
                else:
                    index = self.get_template_index_by_diff_in_region(
                        template_img_4channel_list=self.template_img_4channel_list,
                        top_left_coord=(x, y),
                        size=(w, h),
                    )
                ch = ' ' if index == -1 else '01392846C'[index]
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
    # analyzer.take_snapshot(app_series_no=2)
    # analyzer.get_level_board_size_from_puzzle()
    analyzer.get_levels_str_from_puzzle()
