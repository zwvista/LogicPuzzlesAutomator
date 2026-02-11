from curses.ascii import isdigit
from typing import Self, override

import cv2

from Puzzles.puzzle_analyzer import PuzzleAnalyzer, process_pixel_short_results


class _Analyzer(PuzzleAnalyzer):

    def __init__(self: Self):
        super().__init__(
            400,
            [(1, 5), (21, 6), (61, 7), (101, 8), (141, 9), (181, 10)]
        )

    @override
    def recognize_walls(
            self: Self,
            horizontal_line_list: list[tuple[int, int]],
            vertical_line_list: list[tuple[int, int]]
    ) -> tuple[set[tuple[int, int]], set[tuple[int, int]]]:
        row_walls, col_walls = set(), set()
        h_line, v_line = horizontal_line_list[-1], vertical_line_list[-1]
        end_x, end_y = h_line[0] + h_line[1], v_line[0] + v_line[1]
        for col_idx, (x, w) in enumerate(horizontal_line_list):
            vertical_line_results = self.analyze_vertical_line(x_coord=x+15, start_y=200, end_y=end_y)
            processed_column_grid = process_pixel_short_results(vertical_line_results, is_horizontal=False)
            for row_idx, (y, h) in enumerate(processed_column_grid):
                if row_idx == 0 or row_idx == len(processed_column_grid) - 1 or h > 4:
                    row_walls.add((row_idx, col_idx))

        for row_idx, (y, h) in enumerate(vertical_line_list):
            horizontal_line_results = self.analyze_horizontal_line(y_coord=y+15, start_x=0, end_x=end_x)
            processed_line_grid = process_pixel_short_results(horizontal_line_results, is_horizontal=True)
            for col_idx, (x, w) in enumerate(processed_line_grid):
                if col_idx == 0 or col_idx == len(processed_line_grid) - 1 or w > 4:
                    col_walls.add((row_idx, col_idx))

        return row_walls, col_walls

    @staticmethod
    def format_matrix_with_walls2(
            matrix: list[list[str]],
            walls: tuple[set[tuple[int, int]], set[tuple[int, int]]]
    ) -> str:
        rows, cols = len(matrix) - 1, len(matrix[0]) - 1
        row_walls, col_walls = walls
        lines = []
        for r in range(rows + 1):
            line = []
            for c in range(cols + 1):
                line.append(' ')
                if c == cols: break
                line.append('-' if (r, c) in row_walls else ' ')
            lines.append(''.join(line) + '  `')
            if r == rows: break
            digits = matrix[r]
            line = []
            for c in range(cols + 1):
                line.append('|' if (r, c) in col_walls else ' ')
                if c == cols: break
                line.append(' ')
            lines.append(''.join(line) + digits[cols].rjust(2) + '`')
        digits = matrix[rows]
        line = []
        for c in range(cols):
            line.append(digits[c].rjust(2))
        lines.append(''.join(line) + '   `')
        result = '\n'.join(lines)
        return result

    @override
    def recognize_walls2(
            self: Self,
            horizontal_line_list: list[tuple[int, int]],
            vertical_line_list: list[tuple[int, int]],
            color_b: int = 255,
    ) -> tuple[set[tuple[int, int]], set[tuple[int, int]]]:
        row_walls = set()
        col_walls = set()
        for col_idx, (x, w) in enumerate(horizontal_line_list):
            for row_idx, (y, h) in enumerate(vertical_line_list):
                if row_idx == 0 or sum((1 if self.large_img_bgr[y + dy, x + w // 2][0] == color_b else 0) for dy in range(-2, 3)) > 1:
                    row_walls.add((row_idx, col_idx))
            row_walls.add((len(vertical_line_list), col_idx))

        for row_idx, (y, h) in enumerate(vertical_line_list):
            for col_idx, (x, w) in enumerate(horizontal_line_list):
                if col_idx == 0 or sum((1 if self.large_img_bgr[y + h // 2, x + dx][0] == color_b else 0) for dx in range(-2, 3)) > 1:
                    col_walls.add((row_idx, col_idx))
            col_walls.add((row_idx, len(horizontal_line_list)))

        return row_walls, col_walls

    @override
    def get_level_str_from_image(self: Self) -> str:
        horizontal_lines, vertical_lines = self.get_grid_lines_by_cell_count(self.cell_count + 1)
        horizontal_lines2, vertical_lines2 = horizontal_lines[:-1], vertical_lines[:-1]
        matrix = self.recognize_digits(horizontal_lines, vertical_lines)

        gray = cv2.cvtColor(self.large_img_bgr, cv2.COLOR_BGR2GRAY)
        _, self.large_img_bgr = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
        self.large_img_bgr = cv2.cvtColor(self.large_img_bgr, cv2.COLOR_GRAY2BGR)

        walls = self.recognize_walls2(horizontal_lines2, vertical_lines2)
        level_str = self.format_matrix_with_walls2(matrix, walls)
        return level_str

    @override
    def get_attr_str_from_image(self: Self) -> str:
        text = self.recognize_text(840, 56, 320, 34)
        ch = text[1][-1]
        ch = ch if isdigit(ch) else '4' if ch == ' ' else '1'
        return f' Stitches="{ch}"' if text else ''


if __name__ == "__main__":
    analyzer = _Analyzer()
    # analyzer.take_snapshot(app_series_no=4)
    # analyzer.get_level_board_size_from_puzzle()
    analyzer.get_levels_str_from_puzzle()
