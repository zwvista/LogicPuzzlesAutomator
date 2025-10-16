from typing import Self, override

from Puzzles.puzzle_analyzer import PuzzleAnalyzer, get_template_img_4channel_list, get_level_str_from_matrix


# Games 1 Puzzle Set 12
class _Analyzer(PuzzleAnalyzer):

    SHEEP_PATH = '../../images/128/128_sheep.png'
    WOLF_PATH = '../../images/TileContent/wolf.png'
    template_img_4channel_list = get_template_img_4channel_list(SHEEP_PATH, WOLF_PATH)

    def __init__(self: Self):
        super().__init__(
            100,
            [(1, 5), (5, 6), (11, 7), (23, 8), (39, 9), (59, 10), (79, 11)]
        )

    def recognize_template_and_digits(
            self: Self,
            horizontal_line_list: list[tuple[int, int]],
            vertical_line_list: list[tuple[int, int]]
    ) -> list[list[str]]:
        result = []
        for row_idx, (y, h) in enumerate(vertical_line_list):
            row_result = []
            for col_idx, (x, w) in enumerate(horizontal_line_list):
                horizontal_line_results = self.analyze_horizontal_line(y_coord=y + h // 2, start_x=x, end_x=x+w)
                processed_horizontal_lines = self.process_pixel_long_results(horizontal_line_results, is_horizontal=True, threshold=5)
                if len(processed_horizontal_lines) == 1:
                    ch = ' '
                else:
                    index = self.get_template_index_by_diff_in_region(
                        template_img_4channel_list=self.template_img_4channel_list,
                        top_left_coord=(x, y),
                        size=(w, h),
                    )
                    if index != -1:
                        ch = 'SW'[index]
                    else:
                        ch = self.recognize_digit(x, y, w, h) or ' '
                row_result.append(ch)
            result.append(row_result)
        return result

    @override
    def get_level_str_from_image(self: Self) -> str:
        horizontal_lines, vertical_lines = self.get_grid_lines_by_cell_count(self.cell_count)
        matrix = self.recognize_template_and_digits(horizontal_lines, vertical_lines)
        level_str = get_level_str_from_matrix(matrix)
        return level_str


if __name__ == "__main__":
    analyzer = _Analyzer()
