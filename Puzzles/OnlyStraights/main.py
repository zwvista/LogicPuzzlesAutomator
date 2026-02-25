from typing import Self, override

from Puzzles.puzzle_analyzer import PuzzleAnalyzer, get_level_str_from_matrix


class _Analyzer(PuzzleAnalyzer):

    def __init__(self: Self):
        super().__init__(
            400,
            [(1, 5), (6, 6), (31, 7), (76, 8), (121, 9), (201, 10), (281, 11)]
        )

    def recognize_template(
            self: Self,
            horizontal_line_list: list[tuple[int, int]],
            vertical_line_list: list[tuple[int, int]]
    ) -> list[list[str]]:
        def is_town(color) -> bool:
            return color[0] != 0

        result = []
        for row_idx, (y, h) in enumerate(vertical_line_list):
            row_result = []
            for col_idx, (x, w) in enumerate(horizontal_line_list):
                colors = [(int(c[0]), int(c[1]), int(c[2])) for c in [
                    self.large_img_bgr[y + h // 2, x + w // 2], # center, center
                    self.large_img_bgr[y + h // 2, x + w - 5],  # center, right
                    self.large_img_bgr[y + h - 5, x + w // 2],  # bottom, center
                ]]
                # print(diff_empty, ch)
                b1, b2, b4 = (is_town(colors[0]), is_town(colors[1]), is_town(colors[2]))
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
    # analyzer.take_snapshot(app_series_no=4, start_level=373)
    # analyzer.get_level_board_size_from_puzzle()
    analyzer.get_levels_str_from_puzzle()
