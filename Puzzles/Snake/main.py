from typing import Self, override

from Puzzles.puzzle_analyzer import PuzzleAnalyzer, to_base_36, get_level_str_from_matrix


class _Analyzer(PuzzleAnalyzer):

    def __init__(self: Self):
        super().__init__(
            275,
            [(1, 5), (4, 6), (21, 7), (51, 8), (101, 9), (151, 10)]
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
                    ch = 'S' if self.large_img_bgr[y + h // 2, x + w // 2][0] == 255 else ' '
                row_result.append(ch)
            result.append(row_result)
        return result

    @override
    def get_level_str_from_image(self: Self) -> str:
        horizontal_lines, vertical_lines = self.get_grid_lines_by_cell_count(self.cell_count + 1)
        matrix = self.recognize_pattern(horizontal_lines, vertical_lines)
        level_str = get_level_str_from_matrix(matrix, to_base_36)
        return level_str

    @override
    def get_attr_str_from_image(self: Self) -> str:
        output = self.recognize_text(660, 56, 500, 34)
        return f' SuperTanker="1"' if output else ''


if __name__ == "__main__":
    analyzer = _Analyzer()
    # analyzer.take_snapshot()
    # analyzer.get_level_board_size_from_puzzle()
    analyzer.get_levels_str_from_puzzle()
