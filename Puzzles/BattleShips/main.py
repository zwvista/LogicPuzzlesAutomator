from typing import Self, override

from Puzzles.puzzle_analyzer import PuzzleAnalyzer, to_base_36, get_level_str_from_matrix


# Games 2 Puzzle Set 7
class _Analyzer(PuzzleAnalyzer):

    def __init__(self: Self):
        super().__init__(
            128,
            [(1, 10), (21, 8), (35, 9), (50, 10), (91, 11)]
        )

    def recognize_pattern(
            self: Self,
            horizontal_line_list: list[tuple[int, int]],
            vertical_line_list: list[tuple[int, int]]
    ) -> list[list[str]]:
        def is_gray(y: int, x: int) -> bool:
            b, g, r = self.large_img_bgr[y, x]
            return b == 170

        result = []
        for row_idx, (y, h) in enumerate(vertical_line_list):
            row_result = []
            for col_idx, (x, w) in enumerate(horizontal_line_list):
                if row_idx >= self.cell_count or col_idx >= self.cell_count:
                    ch = self.recognize_digit(x, y, w, h) or ' '
                else:
                    lst = [
                        is_gray(y + 10, x + 10),
                        is_gray(y + 10, x + w - 10),
                        is_gray(y + h - 10, x + w - 10),
                        is_gray(y + h - 10, x + 10),
                        is_gray(y + 10, x + w // 2),
                        is_gray(y + h // 2, x + w // 2),
                    ]
                    ch = '+' if lst[0] and lst[1] and lst[2] and lst[3] else \
                         'v' if lst[0] and lst[1] and not lst[2] and not lst[3] else \
                         '<' if lst[1] and lst[2] and not lst[3] and not lst[0] else \
                         '^' if lst[2] and lst[3] and not lst[0] and not lst[1] else \
                         '>' if lst[3] and lst[0] and not lst[1] and not lst[2] else \
                         'o' if lst[4] and lst[5] and not lst[0] and not lst[1] and not lst[2] and not lst[3] else \
                         '.' if lst[5] and not lst[4] and not lst[0] and not lst[1] and not lst[2] and not lst[3] else \
                         ' '
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
