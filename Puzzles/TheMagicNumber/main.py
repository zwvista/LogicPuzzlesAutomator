from typing import Self, override

from Puzzles.puzzle_analyzer import PuzzleAnalyzer, get_template_img_4channel_list, \
    get_level_str_from_matrix


class _Analyzer(PuzzleAnalyzer):

    PLANTS_PATH = [f'../../images/fruitvegetables/fv ({i}).png' for i in range(1, 78)]
    template_img_4channel_list = get_template_img_4channel_list(*PLANTS_PATH)

    def __init__(self: Self):
        super().__init__(
            400,
            [(1, 6), (51, 9), (171, 12)]
        )
        self.template_img_4channel_list2 = []

    def recognize_small_template(self):
        indexes = []
        for i in range(3):
            index = self.get_template_index_by_diff_in_region(
                template_img_4channel_list=self.template_img_4channel_list,
                top_left_coord=(1082 + 28 * i, 57),
                size=(28, 28),
            ) + 1
            # print(index)
            indexes.append(index)
        self.template_img_4channel_list2 = get_template_img_4channel_list(*(f'../../images/fruitvegetables/fv ({indexes[i]}).png' for i in range(3)))

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
                    template_img_4channel_list=self.template_img_4channel_list2,
                    top_left_coord=(x, y),
                    size=(w, h),
                )
                # if index != -1:
                #     print(f'{row_idx=}, {col_idx=}, {index=}')
                ch = ' ' if index == -1 else 'CBA'[index]
                if sum(1 if c[0] == 136 else 0 for c in [self.large_img_bgr[y + 10, x + 10], self.large_img_bgr[y + 10, x + w - 10]]) > 0:
                    ch = ch.lower()
                row_result.append(ch)
            result.append(row_result)
        return result

    @override
    def get_level_str_from_image(self: Self) -> str:
        self.recognize_small_template()
        horizontal_lines, vertical_lines = self.get_grid_lines_by_cell_count(self.cell_count)
        matrix = self.recognize_template(horizontal_lines, vertical_lines)
        level_str = get_level_str_from_matrix(matrix)
        return level_str


if __name__ == "__main__":
    analyzer = _Analyzer()
    # analyzer.take_snapshot(app_series_no=4, start_level=240)
    # analyzer.get_level_board_size_from_puzzle()
    level_array = [264, 306, 308, 310, 394]
    analyzer.take_snapshot_for_levels(app_series_no=4, level_array=level_array)
    # analyzer.get_levels_str_from_puzzle(336, 391)
    analyzer.get_levels_str_from_puzzle_for_levels(level_array)
