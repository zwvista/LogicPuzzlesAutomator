from typing import Self, override

from Puzzles.puzzle_analyzer import PuzzleAnalyzer, get_template_img_4channel_list, get_level_str_from_matrix


# Games 1 Puzzle Set 11
class _Analyzer(PuzzleAnalyzer):

    RED_PATH = '../../images/TileContent/token_red.png'
    YELLOW_PATH = '../../images/TileContent/token_yellow.png'
    template_img_4channel_list = get_template_img_4channel_list(RED_PATH, YELLOW_PATH)

    def __init__(self: Self):
        super().__init__(
            157,
            [(1,4), (4,5), (7,6), (16,7), (26,8), (38,9), (66,10), (94,11), (126,12)]
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
                ch = ' ' if index == -1 else 'RY'[index]
                row_result.append(ch)
            result.append(row_result)
        return result

    @override
    def get_level_str_from_image(self: Self) -> str:
        horizontal_lines, vertical_lines = self.get_grid_lines_by_cell_count(self.cell_count)
        matrix = self.recognize_template(horizontal_lines, vertical_lines)
        level_str = get_level_str_from_matrix(matrix)
        return level_str


analyzer = _Analyzer()
# analyzer.take_snapshot()
analyzer.get_levels_str_from_puzzle()
