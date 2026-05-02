from typing import Self, override

from Puzzles.puzzle_analyzer import PuzzleAnalyzer, format_matrix_with_walls, get_template_img_4channel_list


class _Analyzer(PuzzleAnalyzer):

    PLANTS_PATH = [f'../../images/fruitvegetables/fv ({i}).png' for i in range(1, 78)]
    template_img_4channel_list = get_template_img_4channel_list(*PLANTS_PATH)

    def __init__(self: Self):
        super().__init__(
            200,
            [(1, 4), (11, 5), (41, 6), (61, 7), (91, 8), (121, 9), (151, 10)]
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

    @override
    def recognize_walls2(
            self: Self,
            horizontal_line_list: list[tuple[int, int]],
            vertical_line_list: list[tuple[int, int]],
            color_b: int = 255,
    ) -> tuple[set[tuple[int, int]], set[tuple[int, int]]]:
        row_walls = set()
        col_walls = set()
        for col_idx, (x, w) in enumerate(horizontal_line_list):
            for row_idx, (y, h) in enumerate(vertical_line_list):
                if row_idx == 0 or sum((1 if self.large_img_bgr[y + dy, x + w // 2][0] > color_b else 0) for dy in range(-3, 4)) > 1:
                    row_walls.add((row_idx, col_idx))
            row_walls.add((len(vertical_line_list), col_idx))

        for row_idx, (y, h) in enumerate(vertical_line_list):
            for col_idx, (x, w) in enumerate(horizontal_line_list):
                if col_idx == 0 or sum((1 if self.large_img_bgr[y + h // 2, x + dx][0] > color_b else 0) for dx in range(-3, 4)) > 1:
                    col_walls.add((row_idx, col_idx))
            col_walls.add((row_idx, len(horizontal_line_list)))

        return row_walls, col_walls

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
                row_result.append(ch)
            result.append(row_result)
        return result

    @override
    def get_level_str_from_image(self: Self) -> str:
        self.recognize_small_template()
        horizontal_lines, vertical_lines = self.get_grid_lines_by_cell_count(self.cell_count)
        matrix = self.recognize_template(horizontal_lines, vertical_lines)
        walls = self.recognize_walls2(horizontal_lines, vertical_lines, 150)
        level_str = format_matrix_with_walls(matrix, walls)
        return level_str


if __name__ == "__main__":
    analyzer = _Analyzer()
    # analyzer.take_snapshot(app_series_no=2)
    # analyzer.get_level_board_size_from_puzzle()
    analyzer.get_levels_str_from_puzzle()
