from typing import Self, override

import cv2

from Puzzles.puzzle_analyzer import PuzzleAnalyzer, to_base_36, get_level_str_from_matrix


class _Analyzer(PuzzleAnalyzer):

    def __init__(self: Self):
        super().__init__(
            185,
            [(1, 10), (46, 11), (126, 12)]
        )

    def get_scale_for_digit_recognition(self: Self, w: int) -> float:
        return 2

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
                     ' '
                ch2 = self.recognize_digit(x, y, w, h)
                horizontal_line_results = self.analyze_horizontal_line(y_coord=y + h // 2, start_x=x + 10, end_x=x + w - 10)
                b = len(horizontal_line_results) == 1
                # print(f'{row_idx=} {col_idx=} {ch=} {ch2=} {b=}')
                ch = ch if ch != ' ' else ' ' if b else ch2 or ' '
                row_result.append(ch)
                if row_idx == 0 and col_idx == 9:
                    roi = self.large_img_rgb[y:y + h, x:x + w]
                    scale = self.get_scale_for_digit_recognition(w)
                    roi_large = cv2.resize(roi, None, fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)

            result.append(row_result)
        return result

    @override
    def get_level_str_from_image(self: Self) -> str:
        horizontal_lines, vertical_lines = self.get_grid_lines_by_cell_count(self.cell_count)

        gray = cv2.cvtColor(self.large_img_rgb, cv2.COLOR_RGB2GRAY)
        _, self.large_img_rgb = cv2.threshold(gray, 140, 255, cv2.THRESH_BINARY)

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
