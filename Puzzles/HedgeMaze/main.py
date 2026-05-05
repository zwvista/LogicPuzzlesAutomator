from typing import Self, override

from Puzzles.puzzle_analyzer import PuzzleAnalyzer, get_template_img_4channel_list, format_matrix_with_walls


class _Analyzer(PuzzleAnalyzer):

    GATE_PATH = '../../images/gates.png'
    STEP_PATH = '../../images/footstep.png'
    FOUNTAIN_PATH = '../../images/fountain.png'
    template_img_4channel_list = get_template_img_4channel_list(GATE_PATH, STEP_PATH, FOUNTAIN_PATH)

    def __init__(self: Self):
        super().__init__(
            200,
            [(1, 4), (3, 5), (11, 6), (41, 7), (71, 8), (111, 9), (151, 10), (191, 11)]
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
                ch = ' ' if index == -1 else 'GSF'[index]
                row_result.append(ch)
            result.append(row_result)
        return result

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
                if row_idx == 0 or sum((1 if abs(self.large_img_bgr[y + dy, x + w // 3][0] - color_b) < 5 else 0) for dy in range(-3, 4)) > 0:
                    row_walls.add((row_idx, col_idx))
            row_walls.add((len(vertical_line_list), col_idx))

        for row_idx, (y, h) in enumerate(vertical_line_list):
            for col_idx, (x, w) in enumerate(horizontal_line_list):
                if col_idx == 0 or sum((1 if abs(self.large_img_bgr[y + h // 3, x + dx][0] - color_b) < 5 else 0) for dx in range(-3, 4)) > 0:
                    col_walls.add((row_idx, col_idx))
            col_walls.add((row_idx, len(horizontal_line_list)))

        return row_walls, col_walls

    @override
    def get_level_str_from_image(self: Self) -> str:
        horizontal_lines, vertical_lines = self.get_grid_lines_by_cell_count(self.cell_count)
        matrix = self.recognize_template(horizontal_lines, vertical_lines)
        walls = self.recognize_walls2(horizontal_lines, vertical_lines, 170)
        level_str = format_matrix_with_walls(matrix, walls)
        return level_str


if __name__ == "__main__":
    analyzer = _Analyzer()
    # analyzer.take_snapshot(app_series_no=2)
    # analyzer.get_level_board_size_from_puzzle()
    analyzer.get_levels_str_from_puzzle()
