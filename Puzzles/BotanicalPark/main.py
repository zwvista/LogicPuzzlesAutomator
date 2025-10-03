from typing import Self, override

from Puzzles.puzzle_analyzer import PuzzleAnalyzer


class Analyzer(PuzzleAnalyzer):

    path_list = [f'../../images/TileContent/arrow{n}.png' for n in list("89632147")]
    template_img_4channel_list = PuzzleAnalyzer.get_template_img_4channel_list(path_list)

    def __init__(self: Self):
        super().__init__("BotanicalPark", False)

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
        horizontal_line_results = self.analyze_horizontal_line(y_coord=210, start_x=0, end_x=1180)
        processed_horizontal_lines = self.process_pixel_long_results(horizontal_line_results, is_horizontal=True)
        cell_length = max(processed_horizontal_lines, key=lambda x: x[1])[1]
        processed_horizontal_lines2, processed_vertical_lines2 = self.get_normalized_lines(cell_length)
        matrix = self.recognize_template(processed_horizontal_lines2, processed_vertical_lines2)
        level_str = '\n'.join([''.join(row) + '`' for row in matrix])
        return level_str

    @override
    def get_attr_str_from_image(self: Self) -> str:
        return ' PlantsInEachArea="2"' if len(self.level_str.split('\n')) >= 9 else ''


analyzer = Analyzer()
analyzer.get_levels_str_from_puzzle(
    1,
    24,
)
