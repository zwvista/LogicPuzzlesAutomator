from typing import Self, override

from Puzzles.puzzle_analyzer import PuzzleAnalyzer, get_template_img_4channel_list, get_level_str_from_matrix


# Games 1 Puzzle Set 17
class _Analyzer(PuzzleAnalyzer):

    CUP_PATH = '../../images/TileContent/cup.png'
    SUGAR_PATH = '../../images/TileContent/cube_white.png'
    template_img_4channel_list = get_template_img_4channel_list(CUP_PATH, SUGAR_PATH)

    def __init__(self: Self):
        super().__init__(
            200,
            [(1,5), (11,6), (31,7), (71,8), (111,9), (151,10), (191,11)]
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
                    tweak=lambda diff_list: [diff_list[0] + 0.03, diff_list[1]],
                )
                ch = ' ' if index == -1 else 'CS'[index]
                row_result.append(ch)
            result.append(row_result)
        return result

    @override
    def get_level_str_from_image(self: Self) -> str:
        horizontal_lines, vertical_lines = self.get_grid_lines_by_cell_count(self.cell_count)
        matrix = self.recognize_template(horizontal_lines, vertical_lines)
        level_str = get_level_str_from_matrix(matrix)
        return level_str

    @override
    def get_attr_str_from_image(self: Self) -> str:
        text = self.recognize_text(840, 56, 320, 34)
        return ' DoubleEspressoVariant="1"' if text else ''


if __name__ == "__main__":
    analyzer = _Analyzer()
