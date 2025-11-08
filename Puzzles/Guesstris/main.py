from typing import Self, override

from Puzzles.puzzle_analyzer import PuzzleAnalyzer, get_template_img_4channel_list, get_level_str_from_matrix


# Games 1 Puzzle Set 10
class _Analyzer(PuzzleAnalyzer):

    SQUARE_PATH = '../../images/bullet_square_green.png'
    TRIANGLE_PATH = '../../images/bullet_triangle_yellow_flat.png'
    CIRCLE_PATH = '../../images/bullet_ball_red.png'
    DIAMOND_PATH = '../../images/bullet_rhombus_blue.png'
    template_img_4channel_list = get_template_img_4channel_list(SQUARE_PATH, TRIANGLE_PATH, CIRCLE_PATH, DIAMOND_PATH)

    def __init__(self: Self):
        super().__init__(
            300,
            [(1, 4), (11, 5), (21, 6), (51, 8), (126, 9), (151, 10), (251, 12)]
        )

    def recognize_template(
            self: Self,
            horizontal_line_list: list[tuple[int, int]],
            vertical_line_list: list[tuple[int, int]]
    ) -> list[list[str]]:
        result = []
        for row_idx, (y, h) in enumerate(vertical_line_list):
            if row_idx == len(vertical_line_list) - 1:
                horizontal_line_results = self.analyze_horizontal_line(y_coord=y + h // 2, start_x=20, end_x=1060)
                if len(horizontal_line_results) == 1:
                    continue
            row_result = []
            for col_idx, (x, w) in enumerate(horizontal_line_list):
                index = self.get_template_index_by_diff_in_region(
                    template_img_4channel_list=self.template_img_4channel_list,
                    top_left_coord=(x, y),
                    size=(w, h),
                )
                ch = ' ' if index == -1 else 'STCD'[index]
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
    analyzer.get_levels_str_from_puzzle()
