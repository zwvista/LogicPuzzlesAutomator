from typing import Self, override

from Puzzles.puzzle_analyzer import PuzzleAnalyzer, get_level_str_from_matrix

block_color = (170, 170, 170)

# Games 1 Puzzle Set 4
class _Analyzer(PuzzleAnalyzer):

    def __init__(self: Self):
        super().__init__(
            24,
            [(1, 4), (3, 5), (5, 6), (7, 7), (9, 8), (11, 9), (13, 10), (24, 11)]
        )

    def recognize_dots(
            self: Self,
            horizontal_line_list: list[tuple[int, int]],
            vertical_line_list: list[tuple[int, int]]
    ) -> list[list[str]]:
        result = []
        for row_idx, (y, h) in enumerate(vertical_line_list):
            row_result = []
            for col_idx, (x, w) in enumerate(horizontal_line_list):
                ch = '>' if self.large_img_bgr[y + h // 2, x + w][0] == 170 else \
                     'x' if self.large_img_bgr[y + h, x + w][0] == 170 else \
                     'v' if self.large_img_bgr[y + h, x + w // 2][0] == 170 else \
                     'o' if self.large_img_bgr[y + h // 2, x + w // 2][0] == 170 else \
                     ' '
                row_result.append(ch)
            result.append(row_result)
        return result


    @override
    def get_level_str_from_image(self: Self) -> str:
        horizontal_lines, vertical_lines = self.get_grid_lines_by_cell_count(self.cell_count)
        matrix = self.recognize_dots(horizontal_lines, vertical_lines)
        level_str = get_level_str_from_matrix(matrix)
        return level_str


if __name__ == "__main__":
    analyzer = _Analyzer()
    # analyzer.take_snapshot()
    # analyzer.get_level_board_size_from_puzzle()
    analyzer.get_levels_str_from_puzzle()
