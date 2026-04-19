from typing import Self, override

from Puzzles.puzzle_analyzer import PuzzleAnalyzer, get_template_img_4channel_list, get_level_str_from_matrix


class _Analyzer(PuzzleAnalyzer):

    UP_PATH = '../../images/arrow8_bw.png'
    RIGHT_PATH = '../../images/arrow6_bw.png'
    DOWN_PATH = '../../images/arrow2_bw.png'
    LEFT_PATH = '../../images/arrow4_bw.png'
    TREASURE_PATH = '../../images/chest_treasure.png'
    template_img_4channel_list = get_template_img_4channel_list(UP_PATH, RIGHT_PATH, DOWN_PATH, LEFT_PATH, TREASURE_PATH)

    def __init__(self: Self):
        super().__init__(
            400,
            [(1, 5), (6, 6), (16, 7), (26, 8), (101, 9), (211, 10), (301, 11)]
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
                ch = ' ' if index == -1 else '^>v<T'[index]
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
