from typing import Self, override

from Puzzles.LightenUp.main import process_matrix_with_blocks
from Puzzles.puzzle_analyzer import PuzzleAnalyzer, get_template_img_4channel_list, get_level_str_from_matrix

block_color = (170, 170, 170)

class _Analyzer(PuzzleAnalyzer):

    FLOWER_PATH = '../../images/flower_blue.png'
    template_img_4channel_list = get_template_img_4channel_list(FLOWER_PATH)

    def __init__(self: Self):
        super().__init__(
            40,
            [(1,4), (3,5), (6,6), (10,7), (14,8), (19,9), (29,10)]
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
                ch = ' ' if index == -1 else 'F'
                row_result.append(ch)
            result.append(row_result)
        return result

    @override
    def get_level_str_from_image(self: Self) -> str:
        horizontal_lines, vertical_lines = self.get_grid_lines_by_cell_count(self.cell_count)
        matrix = self.recognize_template(horizontal_lines, vertical_lines)
        blocks = self.recognize_blocks(horizontal_lines, vertical_lines, lambda color: color == block_color)
        process_matrix_with_blocks(matrix, blocks)
        level_str = get_level_str_from_matrix(matrix)
        return level_str


if __name__ == "__main__":
    analyzer = _Analyzer()
    analyzer.get_levels_str_from_puzzle(12, 12)
