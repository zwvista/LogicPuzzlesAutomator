from typing import Self, override

from Puzzles.puzzle_analyzer import PuzzleAnalyzer, to_base_36, get_level_str_from_matrix


# Games 2 Puzzle Set 7
class _Analyzer(PuzzleAnalyzer):

    def __init__(self: Self):
        super().__init__(
            153,
            [(1, 6), (19, 7), (41, 8), (63, 9), (64, 10), (89, 11), (113, 12), (134, 14)]
        )

    def recognize_pattern(
            self: Self,
            horizontal_line_list: list[tuple[int, int]],
            vertical_line_list: list[tuple[int, int]]
    ) -> list[list[str]]:
        result = []
        for row_idx, (y, h) in enumerate(vertical_line_list):
            row_result = []
            for col_idx, (x, w) in enumerate(horizontal_line_list):
                if row_idx >= self.cell_count or col_idx >= self.cell_count:
                    ch = self.recognize_digit(x, y, w, h) or ' '
                else:
                    color = self.large_img_bgr[y + 20, x + 20]
                    ch = 'C' if color[0] == 170 else ' '
                row_result.append(ch)
            result.append(row_result)
        return result

    @override
    def get_level_str_from_image(self: Self) -> str:
        horizontal_lines, vertical_lines = self.get_grid_lines_by_cell_count(self.cell_count + 1)
        matrix = self.recognize_pattern(horizontal_lines, vertical_lines)
        level_str = get_level_str_from_matrix(matrix, to_base_36)
        return level_str


if __name__ == "__main__":
    analyzer = _Analyzer()
    analyzer.take_snapshot()
    analyzer.get_level_board_size_from_puzzle()
    # analyzer.get_levels_str_from_puzzle()
