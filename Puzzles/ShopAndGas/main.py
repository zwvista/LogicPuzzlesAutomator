from typing import Self, override

from Puzzles.puzzle_analyzer import PuzzleAnalyzer, get_template_img_4channel_list, get_level_str_from_matrix


# Games 1 Puzzle Set 10
class _Analyzer(PuzzleAnalyzer):

    HOME_PATH = '../../images/TileContent/home.png'
    SHOP_PATH = '../../images/TileContent/shoppingcart.png'
    GAS_PATH = '../../images/TileContent/gauge.png'
    template_img_4channel_list = get_template_img_4channel_list(HOME_PATH, SHOP_PATH, GAS_PATH)

    def __init__(self: Self):
        super().__init__(
            36,
            [(1,5), (5,6), (9,7), (16,8), (23,9), (30,10)],
            False
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
                ch = ' ' if index == -1 else 'HSG'[index]
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
analyzer.get_levels_str_from_puzzle(12, 12)
