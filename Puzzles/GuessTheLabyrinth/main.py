from typing import Self, override

from Puzzles.puzzle_analyzer import PuzzleAnalyzer, get_level_str_from_matrix


class _Analyzer(PuzzleAnalyzer):

    def __init__(self: Self):
        super().__init__(
            300,
            [(1, 4), (3, 6), (31, 7), (61, 8), (141, 9), (181, 10), (281, 11)]
        )

    def recognize_dots(
            self: Self,
            horizontal_line_list: list[tuple[int, int]],
            vertical_line_list: list[tuple[int, int]]
    ) -> list[list[str]]:
        def has_dot(x: int, y: int) -> bool:
            for dx in range(-2, 3):
                for dy in range(-2, 3):
                    if 0 <= x + dx < 1182:
                        b, g, r = self.large_img_bgr[y + dy, x + dx]
                        if b == 255 and g == 255 and r == 255:
                            return True
            return False

        result = []
        for row_idx, (y, h) in enumerate(vertical_line_list):
            row_result = []
            for col_idx, (x, w) in enumerate(horizontal_line_list):
                row_result.append('O' if has_dot(x, y) else ' ')
                row_result.append(' ' if row_idx > 0 else '-')
            row_result.append('O' if has_dot(x + w, y) else ' ')
            result.append(row_result)

            row_result = ['|']
            for col_idx, (x, w) in enumerate(horizontal_line_list):
                ch = ' '
                if col_idx > 0:
                    row_result.append(' ')
                row_result.append(ch)
            row_result.append('|')
            result.append(row_result)

        row_result = []
        for col_idx, (x, w) in enumerate(horizontal_line_list):
            row_result.append('O' if has_dot(x, y + h) else ' ')
            row_result.append('-')
        row_result.append('O' if has_dot(x + w, y + h) else ' ')
        result.append(row_result)

        return result


    @override
    def get_level_str_from_image(self: Self) -> str:
        horizontal_lines, vertical_lines = self.get_grid_lines_by_cell_count(self.cell_count)
        horizontal_line_results = self.analyze_horizontal_line(1370, 20, 1170)
        if len(horizontal_line_results) == 1:
            vertical_lines = vertical_lines[:-1]
        matrix = self.recognize_dots(horizontal_lines, vertical_lines)
        level_str = get_level_str_from_matrix(matrix)
        return level_str


if __name__ == "__main__":
    analyzer = _Analyzer()
    # analyzer.take_snapshot(app_series_no=3)
    # analyzer.get_level_board_size_from_puzzle()
    analyzer.get_levels_str_from_puzzle()
