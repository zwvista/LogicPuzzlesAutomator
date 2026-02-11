from typing import Self, override

import cv2

from Puzzles.puzzle_analyzer import PuzzleAnalyzer, get_template_img_4channel_list


class _Analyzer(PuzzleAnalyzer):

    RED_PATH = '../../images/nav_plain_red.png'
    GREEN_PATH = '../../images/nav_plain_green.png'
    template_img_4channel_list = get_template_img_4channel_list(RED_PATH, GREEN_PATH)

    def __init__(self: Self):
        super().__init__(
            400,
            [(1, 5), (6, 6), (21, 7), (66, 8), (126, 9), (186, 10), (281, 11)]
        )

    def recognize_template(
            self: Self,
            horizontal_line_list: list[tuple[int, int]],
            vertical_line_list: list[tuple[int, int]]
    ) -> list[list[str]]:
        result = []
        for row_idx, (y, h) in enumerate(vertical_line_list):
            row_result = []
            for col_idx, (x, w) in enumerate(horizontal_line_list):
                index = self.get_template_index_by_diff_in_region(
                    template_img_4channel_list=self.template_img_4channel_list,
                    top_left_coord=(x, y),
                    size=(w, h),
                )
                ch = ' ' if index == -1 else 'RGY'[index]
                row_result.append(ch)
            result.append(row_result)
        return result

    @override
    def recognize_digit(self: Self, x: int, y: int, w: int, h: int) -> str | None:
        roi = self.large_img_rgb[y:y + h, x:x + w]
        scale = self.get_scale_for_digit_recognition(w)
        roi_large = cv2.resize(roi, None, fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)
        output = self.reader.readtext(roi_large)
        if not output:
            return None
        else:
            _, text, prob = output[0]
            if text == "22":
                if prob < 0.99:
                    text = "2"
            return text

    @staticmethod
    def format_matrix_with_digits(
            matrix: list[list[str]],
            matrix2: list[list[str]]
    ) -> str:
        rows, cols = len(matrix), len(matrix[0])
        lines = []
        for r in range(rows):
            line = []
            lights = matrix[r]
            digits = matrix2[r]
            for c in range(cols):
                l = lights[c]; d = digits[c]
                if l != " ":
                    if d[0] == "(":
                        d = d[1] if len(d) > 1 else ' '
                    if not d.isdigit():
                        d = "B" if l == "R" else "W" if l == "G" else " "
                line.append(l + d)
            lines.append(''.join(line) + '`')
        result = '\n'.join(lines)
        return result

    @override
    def get_level_str_from_image(self: Self) -> str:
        horizontal_lines, vertical_lines = self.get_grid_lines_by_cell_count(self.cell_count)
        matrix = self.recognize_template(horizontal_lines, vertical_lines)

        gray = cv2.cvtColor(self.large_img_bgr, cv2.COLOR_BGR2GRAY)
        _, self.large_img_bgr = cv2.threshold(gray, 10, 255, cv2.THRESH_BINARY)
        self.large_img_bgr = cv2.cvtColor(self.large_img_bgr, cv2.COLOR_GRAY2BGR)

        matrix2 = self.recognize_digits(horizontal_lines, vertical_lines)
        level_str = self.format_matrix_with_digits(matrix, matrix2)
        return level_str


if __name__ == "__main__":
    analyzer = _Analyzer()
    # analyzer.take_snapshot(app_series_no=4)
    # analyzer.get_level_board_size_from_puzzle()
    analyzer.get_levels_str_from_puzzle()
