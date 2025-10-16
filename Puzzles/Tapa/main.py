from typing import Self, override

import cv2

from Puzzles.puzzle_analyzer import PuzzleAnalyzer, get_level_str_from_matrix


class TapaBaseAnalyzer(PuzzleAnalyzer):

    # @override
    def recognize_digit2(self: Self, r: int, c: int, x: int, y: int, w: int, h: int) -> str | None:
        roi = self.large_img_rgb[y:y + h, x:x + w]
        scale = 2 if w > 180 else 4
        roi_large = cv2.resize(roi, None, fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)
        output = self.reader.readtext(roi_large)
        if output:
            # for _, text, prob in output:
            #     if text == "2" and prob < 0.99:
            #         print(f"{r=}, {c=}, len={len(output)}, prob={float(prob):.3f}")
            threshold = 0.98 if w > 200 else 0.99
            output = [('2' if text == "22" else '?' if text == '2' and prob < threshold else text)  for _, text, prob in output]
            output_str = ''.join(output)
        else:
            output_str = ''
        return output_str.ljust(4)

    @override
    def recognize_digits(
            self: Self,
            horizontal_line_list: list[tuple[int, int]],
            vertical_line_list: list[tuple[int, int]]
    ) -> list[list[str]]:
        self.large_img_rgb = cv2.cvtColor(self.large_img_rgb, cv2.COLOR_BGR2GRAY)
        result = []
        for row_idx, (y, h) in enumerate(vertical_line_list):
            row_result = []
            for col_idx, (x, w) in enumerate(horizontal_line_list):
                ch = self.recognize_digit2(row_idx, col_idx, x, y, w, h) or [' ']
                row_result.append(ch)
            result.append(row_result)
        return result

    @override
    def get_level_str_from_image(self: Self) -> str:
        # print(f'{self.current_level=}, {self.cell_count=}')
        horizontal_lines, vertical_lines = self.get_grid_lines_by_cell_count(self.cell_count)
        matrix = self.recognize_digits(horizontal_lines, vertical_lines)
        level_str = get_level_str_from_matrix(matrix)
        return level_str


# Games 1 Puzzle Set 10
class _Analyzer(TapaBaseAnalyzer):

    def __init__(self: Self):
        super().__init__(
            67,
            [(1,5), (4,6), (12,7), (20,8), (28,9), (36,10)]
        )

    @override
    def get_attr_str_from_image(self: Self) -> str:
        text = self.recognize_text(660, 56, 500, 34)
        return f' GameType="{text}"' if text else ''


if __name__ == "__main__":
    analyzer = _Analyzer()
    analyzer.get_levels_str_from_puzzle()
