from typing import Self, override

from Puzzles.puzzle_analyzer import PuzzleAnalyzer, get_template_img_4channel_list, get_level_str_from_matrix


# Games 1 Puzzle Set 12
class _Analyzer(PuzzleAnalyzer):

    paths = (f'../../images/TileContent/arrow{n}.png' for n in "89632147")
    template_img_4channel_list = get_template_img_4channel_list(*paths)

    def __init__(self: Self):
        super().__init__(
            24,
            [(1,5), (4,6), (7,7), (10,8), (13,9), (16,10), (19,11), (22,12)],
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
                horizontal_line_results = self.analyze_horizontal_line(y_coord=y + h // 2, start_x=x, end_x=x+w)
                processed_horizontal_lines = self.process_pixel_long_results(horizontal_line_results, is_horizontal=True)
                if len(processed_horizontal_lines) == 1:
                    index = -1
                else:
                    index = self.get_template_index_by_diff_in_region(
                        template_img_4channel_list=self.template_img_4channel_list,
                        top_left_coord=(x, y),
                        size=(w, h),
                    )
                ch = ' ' if index == -1 else str(index)
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
        return ' PlantsInEachArea="2"' if self.cell_count >= 9 else ''


analyzer = _Analyzer()
analyzer.get_levels_str_from_puzzle()
