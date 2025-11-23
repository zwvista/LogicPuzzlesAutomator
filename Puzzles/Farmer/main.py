from typing import Self, override

from Puzzles.puzzle_analyzer import PuzzleAnalyzer, format_matrix_with_walls, get_template_img_4channel_list


# Games 2 Puzzle Set 2
class _Analyzer(PuzzleAnalyzer):

    PLANT_A1_PATH = '../../images/aubergine.png'
    PLANT_B1_PATH = '../../images/carrot.png'
    PLANT_C1_PATH = '../../images/C3.png'
    template_img_4channel_list = get_template_img_4channel_list(PLANT_A1_PATH, PLANT_B1_PATH)

    def __init__(self: Self):
        super().__init__(
            200,
            [(1, 6), (11, 7), (41, 8), (81, 9), (121, 10), (161, 11), (181, 12)]
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
                ch = ' ' if index != 1 else 'O'
                row_result.append(ch)
            result.append(row_result)
        return result

    @override
    def get_level_str_from_image(self: Self) -> str:
        horizontal_lines, vertical_lines = self.get_grid_lines_by_cell_count(self.cell_count)
        matrix = self.recognize_template(horizontal_lines, vertical_lines)
        walls = self.recognize_walls2(horizontal_lines, vertical_lines, 0)
        level_str = format_matrix_with_walls(matrix, walls)
        return level_str


if __name__ == "__main__":
    analyzer = _Analyzer()
    # analyzer.take_snapshot(app_series_no=2)
    # analyzer.get_level_board_size_from_puzzle()
    analyzer.get_levels_str_from_puzzle()
