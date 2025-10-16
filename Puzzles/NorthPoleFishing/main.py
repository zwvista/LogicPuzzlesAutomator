from typing import override

from typing_extensions import Self

from Puzzles.puzzle_analyzer import PuzzleAnalyzer, get_template_img_4channel_list, get_level_str_from_matrix


# Games 1 Puzzle Set 14
class _Analyzer(PuzzleAnalyzer):

    CUBE_PATH = '../../images/128/128_icecube.png'
    HOLE_PATH = '../../images/TileContent/ice_hole.png'
    template_img_4channel_list = get_template_img_4channel_list(CUBE_PATH, HOLE_PATH)

    def __init__(self: Self):
        super().__init__(
            200,
            [(1,4), (11,5), (41,6), (81,7), (111,8), (151,9), (181,10)]
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
                horizontal_line_results = self.analyze_horizontal_line(y_coord=y + h // 2, start_x=x, end_x=x+w)
                if len(horizontal_line_results) == 1:
                    index = -1
                else:
                    index = self.get_template_index_by_diff_in_region(
                        template_img_4channel_list=self.template_img_4channel_list,
                        top_left_coord=(x, y),
                        size=(w, h),
                    )
                ch = ' ' if index == -1 else 'BH'[index]
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
