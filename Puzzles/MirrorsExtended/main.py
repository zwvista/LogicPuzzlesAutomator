from typing import Self, override

import cv2

from Puzzles.puzzle_analyzer import PuzzleAnalyzer, process_pixel_short_results


class _Analyzer(PuzzleAnalyzer):

    def __init__(self: Self):
        super().__init__(
            200,
            [(1, 4), (11, 5), (41, 6), (71, 7), (116, 8), (146, 9), (176, 10)]
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
            if col_idx == 0: continue
            vertical_line_results = self.analyze_vertical_line(x_coord=x+15, start_y=200, end_y=end_y)
            processed_column_grid = process_pixel_short_results(vertical_line_results, is_horizontal=False)
            for row_idx, (y, h) in enumerate(processed_column_grid):
                if row_idx == 1 or row_idx == len(processed_column_grid) - 1 or h > 4:
                    row_walls.add((row_idx, col_idx))

        for row_idx, (y, h) in enumerate(vertical_line_list):
            if row_idx == 0: continue
            horizontal_line_results = self.analyze_horizontal_line(y_coord=y+15, start_x=0, end_x=end_x)
            processed_line_grid = process_pixel_short_results(horizontal_line_results, is_horizontal=True)
            for col_idx, (x, w) in enumerate(processed_line_grid):
                if col_idx == 1 or col_idx == len(processed_line_grid) - 1 or w > 4:
                    col_walls.add((row_idx, col_idx))

        return row_walls, col_walls

    def recognize_text2(self: Self, x: int, y: int, w: int, h: int) -> str | None:
        roi = self.large_img_rgb[y:y + h, x:x + w]
        scale = self.get_scale_for_digit_recognition(w)
        roi_large = cv2.resize(roi, None, fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)
        output = self.reader.readtext(roi_large)
        if not output:
            return None
        else:
            _, text, prob = output[0]
            return text

    def recognize_texts(
            self: Self,
            horizontal_line_list: list[tuple[int, int]],
            vertical_line_list: list[tuple[int, int]]
    ) -> list[list[str]]:
        result = []
        for row_idx, (y, h) in enumerate(vertical_line_list):
            row_result = []
            for col_idx, (x, w) in enumerate(horizontal_line_list):
                horizontal_line_results = self.analyze_horizontal_line(y_coord=y + h // 2, start_x=x + 10, end_x=x+w - 10)
                if len(horizontal_line_results) == 1:
                    ch = '  '
                else:
                    ch = self.recognize_text2(x, y, w, h) or '  '
                row_result.append(ch)
            result.append(row_result)
        return result

    @staticmethod
    def format_matrix_with_walls2(
            matrix: list[list[str]],
            walls: tuple[set[tuple[int, int]], set[tuple[int, int]]]
    ) -> str:
        rows, cols = len(matrix), len(matrix[0])
        row_walls, col_walls = walls
        lines = []

        def f(r: int) -> None:
            line = []
            texts = matrix[r]
            for c in range(cols):
                if c == cols - 1:
                    line.append(' ')
                line.append(texts[c])
            lines.append(''.join(line) + '`')

        f(0)
        for r in range(1, rows):
            line = []
            for c in range(cols):
                line.append(' -' if (r, c) in row_walls else '  ')
            lines.append(''.join(line) + ' `')
            if r == rows - 1: break
            texts = matrix[r]
            line = [texts[0]]
            for c in range(1, cols):
                line.append('|' if (r, c) in col_walls else ' ')
                if c == cols - 1: break
                line.append(' ')
            lines.append(''.join(line) + texts[cols - 1] + '`')
        f(rows - 1)
        result = '\n'.join(lines)
        return result

    @override
    def get_level_str_from_image(self: Self) -> str:
        horizontal_lines, vertical_lines = self.get_grid_lines_by_cell_count(self.cell_count + 2)
        horizontal_lines2, vertical_lines2 = horizontal_lines[:-1], vertical_lines[:-1]
        matrix = self.recognize_texts(horizontal_lines, vertical_lines)
        walls = self.recognize_walls(horizontal_lines2, vertical_lines2)
        level_str = self.format_matrix_with_walls2(matrix, walls)
        return level_str


if __name__ == "__main__":
    analyzer = _Analyzer()
    # analyzer.take_snapshot(app_series_no=2)
    # analyzer.get_level_board_size_from_puzzle()
    analyzer.get_levels_str_from_puzzle()
