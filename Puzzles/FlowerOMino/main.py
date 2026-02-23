from typing import Self, override

from Puzzles.puzzle_analyzer import PuzzleAnalyzer, get_template_img_4channel_list, get_level_str_from_matrix


class _Analyzer(PuzzleAnalyzer):

    FLOWER_PATH = '../../images/flower_blue.png'
    template_img_4channel_list = get_template_img_4channel_list(FLOWER_PATH)

    def __init__(self: Self):
        super().__init__(
            400,
            [(1, 4), (11, 5), (31, 6), (51, 7), (131, 8), (171, 9), (231, 10), (351, 11)]
        )

    def recognize_template(
            self: Self,
            horizontal_line_list: list[tuple[int, int]],
            vertical_line_list: list[tuple[int, int]]
    ) -> list[list[str]]:
        def is_red(color) -> bool:
            return 138 <= color[0] <= 167 and 138 <= color[2] <= 167
        def is_flower(color) -> bool:
            return color[0] != 0 and not is_red(color)

        result = []
        for row_idx, (y, h) in enumerate(vertical_line_list):
            row_result = []
            for col_idx, (x, w) in enumerate(horizontal_line_list):
                colors = [(int(c[0]), int(c[1]), int(c[2])) for c in [
                    self.large_img_bgr[y + h // 2, x + 3], # center, left
                    self.large_img_bgr[y + h // 2, x + w - 3], # center, right
                    self.large_img_bgr[y + h - 3, x + w // 2], # bottom, center
                    self.large_img_bgr[y + 3, x + w // 2],  # top, center
                    self.large_img_bgr[y + h // 2, x + w // 2], # center, center
                    self.large_img_bgr[y + h // 2 - 10, x + w - 3],  # center2, right
                    self.large_img_bgr[y + h - 3, x + w // 2 + 10],  # bottom, center2
                ]]
                # print(f'{row_idx=}, {col_idx=}, {x=}, {y=}, {w=}, {h=}, {colors=}')
                if (is_red(colors[0]) and (is_red(colors[1]) or is_red(colors[5])) and
                        (is_red(colors[2]) or is_red(colors[6])) and is_red(colors[3])):
                    ch = '='
                else:
                    b1, b2, b4 = (is_flower(colors[4]), is_flower(colors[1]) or is_flower(colors[5]),
                                  is_flower(colors[2]) or is_flower(colors[6]))
                    n = (1 if b1 else 0) + (2 if b2 else 0) + (4 if b4 else 0)
                    ch = ' ' if n == 0 else str(n)
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
    # analyzer.take_snapshot(app_series_no=4)
    # analyzer.get_level_board_size_from_puzzle()
    analyzer.get_levels_str_from_puzzle()
