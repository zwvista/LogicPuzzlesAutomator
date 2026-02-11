from typing import Self, override

from Puzzles.puzzle_analyzer import PuzzleAnalyzer, get_template_img_4channel_list, get_level_str_from_matrix


class _Analyzer(PuzzleAnalyzer):

    PIPE_UR_PATH = '../../images/pipe_1.png'
    PIPE_RD_PATH = '../../images/pipe_2.png'
    PIPE_DL_PATH = '../../images/pipe_3.png'
    PIPE_LU_PATH = '../../images/pipe_4.png'
    PIPE_CROSS_PATH = '../../images/pipe_cross.png'
    PIPE_LR_PATH = '../../images/pipe_horizontal.png'
    PIPE_UD_PATH = '../../images/pipe_vertical.png'
    template_img_4channel_list = get_template_img_4channel_list(PIPE_UR_PATH, PIPE_RD_PATH, PIPE_DL_PATH, PIPE_LU_PATH, PIPE_CROSS_PATH, PIPE_LR_PATH, PIPE_UD_PATH)

    def __init__(self: Self):
        super().__init__(
            200,
            [(1, 5), (21, 6), (41, 7), (71, 8), (111, 9), (151, 10)]
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
                ch = ' ' if index == -1 else '36C9FA5'[index]
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
