from typing import Self, override

from Puzzles.puzzle_analyzer import PuzzleAnalyzer, to_base_36, get_level_str_from_matrix


# Games 2 Puzzle Set 7
class _Analyzer(PuzzleAnalyzer):

    def __init__(self: Self):
        super().__init__(
            45,
            [(1, 7), (8, 8), (15, 9), (22, 10), (29, 11), (36, 12)]
        )

    def recognize_pattern(
            self: Self,
            horizontal_line_list: list[tuple[int, int]],
            vertical_line_list: list[tuple[int, int]]
    ) -> list[list[str]]:
        def is_gray(y: int, x: int, check3: bool) -> bool:
            b1, _, _ = self.large_img_bgr[y, x]
            b2, _, _ = self.large_img_bgr[y, x - 1]
            b3, _, _ = self.large_img_bgr[y, x + 1]
            return b1 != 0 and (not check3 or (b2 != 0 and b3 != 0))

        result = []
        for row_idx, (y, h) in enumerate(vertical_line_list):
            row_result = []
            for col_idx, (x, w) in enumerate(horizontal_line_list):
                lst = [
                    is_gray(y + h // 4, x + w // 4, True),
                    is_gray(y + h // 4, x + w // 2, False),
                    is_gray(y + h // 4, x + w - w // 4, True),
                    is_gray(y + h // 2, x + w - w // 4, False),
                    is_gray(y + h - h // 4, x + w - w // 4, True),
                    is_gray(y + h - h // 4, x + w // 2, False),
                    is_gray(y + h - h // 4, x + w // 4, True),
                    is_gray(y + h // 2, x + w // 4, False),
                ]
                ch = 'S' if self.large_img_bgr[y + h // 2, x + w // 2][1] == 202 else \
                     '9' if not lst[0] and lst[7] and lst[1] and lst[4] else \
                     '3' if not lst[2] and lst[1] and lst[3] and lst[6] else \
                     '6' if not lst[4] and lst[3] and lst[5] and lst[0] else \
                     'C' if not lst[6] and lst[5] and lst[7] and lst[2] else \
                     '5' if lst[1] and not lst[0] and not lst[2] and not lst[4] and not lst[6] else \
                     'A' if lst[3] and not lst[0] and not lst[2] and not lst[4] and not lst[6] else \
                     'O' if lst[0] and lst[2] and lst[4] and lst[6] else \
                     ' '
                row_result.append(ch)
            result.append(row_result)
        return result

    @override
    def get_level_str_from_image(self: Self) -> str:
        horizontal_lines, vertical_lines = self.get_grid_lines_by_cell_count(self.cell_count)
        matrix = self.recognize_pattern(horizontal_lines, vertical_lines)
        level_str = get_level_str_from_matrix(matrix, to_base_36)
        return level_str


if __name__ == "__main__":
    analyzer = _Analyzer()
    # analyzer.take_snapshot()
    # analyzer.get_level_board_size_from_puzzle()
    analyzer.get_levels_str_from_puzzle()
