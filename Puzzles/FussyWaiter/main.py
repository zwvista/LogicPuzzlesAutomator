from typing import Self, override

from Puzzles.puzzle_analyzer import PuzzleAnalyzer, get_template_img_4channel_list, get_level_str_from_matrix


class _Analyzer(PuzzleAnalyzer):
    FOODS_PATH = [
        '../../images/FW_aX.png',# hamburger
        '../../images/FW_bX.png',# pizza
        '../../images/FW_cX.png',# fries
        '../../images/FW_dX.png',# donut
        '../../images/FW_eX.png',# fish
        '../../images/FW_fX.png',# icecream
        '../../images/FW_gX.png',# pig
        '../../images/FW_sX.png',#
    ]
    DRINKS_PATH = [
        '../../images/FW_XA.png',# drink_blue
        '../../images/FW_XB.png',# cup
        '../../images/FW_XC.png',# wine_red_glass
        '../../images/FW_XD.png',# beer_glass
        '../../images/FW_XE.png',# cocktail
        '../../images/FW_XF.png',# wine_white_glass
        '../../images/FW_XG.png',# lemonade_bottle
        '../../images/FW_XS.png',#
    ]
    template_img_4channel_list_foods = get_template_img_4channel_list(*FOODS_PATH)
    template_img_4channel_list_drinks = get_template_img_4channel_list(*DRINKS_PATH)

    def __init__(self: Self):
        super().__init__(
            141,
            [(1, 3), (7, 4), (51, 5), (111, 7)]
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
                index1 = self.get_template_index_by_diff_in_region(
                    template_img_4channel_list=self.template_img_4channel_list_foods,
                    top_left_coord=(x, y),
                    size=(w // 2, h),
                    tweak=lambda diff_list: [dl + 0.02 if i == 7 else dl for (i, dl) in enumerate(diff_list)],
                )
                index2 = self.get_template_index_by_diff_in_region(
                    template_img_4channel_list=self.template_img_4channel_list_drinks,
                    top_left_coord=(x + w // 2, y),
                    size=(w // 2, h),
                )
                # print(f'{row_idx=}, {col_idx=}, {index1=}, {index2=}')
                ch = (' ' if index1 == -1 else 'abcdefg '[index1]) + (' ' if index2 == -1 else 'ABCDEFG '[index2])
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
    # analyzer.take_snapshot()
    # analyzer.get_level_board_size_from_puzzle()
    analyzer.get_levels_str_from_puzzle()
