from typing import Self, override

from Puzzles.puzzle_analyzer import PuzzleAnalyzer, get_template_img_4channel_list, get_level_str_from_matrix


class _Analyzer(PuzzleAnalyzer):
    SHEEP_PATH = '../../images/sheep2.png'
    WOLF_PATH = '../../images/wolf2.png'
    template_img_4channel_list = get_template_img_4channel_list(SHEEP_PATH, WOLF_PATH)

    def __init__(self: Self):
        super().__init__(
            200,
            [(1, 5), (21, 6), (41, 7), (91, 8), (131, 9), (191, 10)]
        )

    def recognize_template(
            self: Self,
            horizontal_line_list: list[tuple[int, int]],
            vertical_line_list: list[tuple[int, int]]
    ) -> list[list[str]]:
        result = []

        row_result = []
        for col_idx in range(len(horizontal_line_list)):
            row_result.append(' '); row_result.append('-')
        row_result.append(' ')
        result.append(row_result)

        for row_idx, (y, h) in enumerate(vertical_line_list):
            if row_idx > 0:
                row_result = [' ']
                for col_idx, (x, w) in enumerate(horizontal_line_list):
                    if col_idx > 0:
                        colors = (self.large_img_bgr[y + dy, x + dx][0] == 255 for dy in range(0, 1) for dx in range(0, 1))
                        row_result.append('O' if all(colors) else ' ')
                    row_result.append(' ')
                row_result.append(' ')
                result.append(row_result)

            row_result = ['|']
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
                ch = ' ' if index == -1 else 'SW'[index]
                if col_idx > 0:
                    row_result.append(' ')
                row_result.append(ch)
            row_result.append('|')
            result.append(row_result)

        row_result = []
        for col_idx in range(len(horizontal_line_list)):
            row_result.append(' '); row_result.append('-')
        row_result.append(' ')
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
    # analyzer.take_snapshot(app_series_no=2)
    # analyzer.get_level_board_size_from_puzzle()
    analyzer.get_levels_str_from_puzzle()
