from typing import Self, override

from Puzzles.puzzle_analyzer import PuzzleAnalyzer, get_template_img_4channel_list, get_level_str_from_matrix


class _Analyzer(PuzzleAnalyzer):

    DIFF_PATH = '../../images/carpenter_different.png'
    EQUAL_PATH = '../../images/carpenter_equal.png'
    QM_PATH = '../../images/carpenter_help.png'
    template_img_4channel_list = get_template_img_4channel_list(DIFF_PATH, EQUAL_PATH, QM_PATH)

    def __init__(self: Self):
        super().__init__(
            300,
            [(1, 5), (21, 6), (51, 7), (91, 8), (151, 9), (196, 10), (241, 11)]
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
                # dl = [self.get_template_diff_in_region(
                #     template_img_4channel=template_img_4channel,
                #     top_left_coord=(x, y),
                #     size=(w, h)
                # ) for template_img_4channel in self.template_img_4channel_list]
                # print(f'{row_idx}. {col_idx}: {dl}')
                index = self.get_template_index_by_diff_in_region(
                    template_img_4channel_list=self.template_img_4channel_list,
                    top_left_coord=(x, y),
                    size=(w, h),
                    tweak=lambda diff_list: [diff_list[0], diff_list[1] + 0.03, diff_list[2]]
                )
                ch = ' ' if index == -1 else '/=?'[index]
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
    # analyzer.take_snapshot(app_series_no=3)
    # analyzer.get_level_board_size_from_puzzle()
    analyzer.get_levels_str_from_puzzle(158)
