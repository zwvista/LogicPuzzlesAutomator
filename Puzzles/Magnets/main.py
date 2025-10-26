import math
from typing import Self, override

from Puzzles.puzzle_analyzer import PuzzleAnalyzer, process_pixel_short_results, get_level_str_from_matrix


# Games 1 Puzzle Set 2
class _Analyzer(PuzzleAnalyzer):

    def __init__(self: Self):
        super().__init__(
            119,
            [(1, 4), (3, 5), (11, 6), (28, 7), (38, 8), (66, 9), (82, 10)]
        )

    def recognize_walls2(
            self: Self,
            horizontal_line_list: list[tuple[int, int]],
            vertical_line_list: list[tuple[int, int]]
    ) -> tuple[set[tuple[int, int]], set[tuple[int, int]]]:
        row_walls = set()
        col_walls = set()
        sz = vertical_line_list[0][1]
        end_y = 1400 - sz * 2
        end_x = 1200 - sz * 2
        for col_idx, (x, w) in enumerate(horizontal_line_list):
            vertical_line_results = self.analyze_vertical_line(x_coord=x+w//2, start_y=200, end_y=end_y)
            processed_column_grid = process_pixel_short_results(vertical_line_results, is_horizontal=False)
            for (y, h) in processed_column_grid:
                if y is None: continue
                row_idx = math.floor((y - 200) / sz + .2)
                row_walls.add((row_idx, col_idx))

        for row_idx, (y, h) in enumerate(vertical_line_list):
            horizontal_line_results = self.analyze_horizontal_line(y_coord=y+h//2, start_x=0, end_x=end_x)
            processed_line_grid = process_pixel_short_results(horizontal_line_results, is_horizontal=True)
            for (x, w) in processed_line_grid:
                if x is None: continue
                col_idx = math.floor(x / sz + .2)
                col_walls.add((row_idx, col_idx))

        return row_walls, col_walls

    @staticmethod
    def format_matrix_with_walls2(
            matrix: list[list[str]],
            walls: tuple[set[tuple[int, int]], set[tuple[int, int]]]
    ) -> None:
        rows, cols = len(matrix), len(matrix[0])
        row_walls, col_walls = walls
        positions = set()
        for r in range(rows - 1):
            for c in range(cols - 1):
                if (r, c) in positions: continue
                bh = (r, c + 1) in col_walls
                bv = (r + 1, c) in row_walls
                if bh and bv:
                    positions.add((r, c))
                    matrix[r][c] = '.'
                elif bh:
                    positions.add((r, c))
                    positions.add((r + 1, c))
                    matrix[r][c] = 'V'
                elif bv:
                    positions.add((r, c))
                    positions.add((r, c + 1))
                    matrix[r][c] = 'H'
        matrix[rows - 2][cols - 2] = '+'
        matrix[rows - 1][cols - 1] = '-'

    @override
    def get_level_str_from_image(self: Self) -> str:
        horizontal_lines, vertical_lines = self.get_grid_lines_by_cell_count(self.cell_count + 2)
        matrix = self.recognize_digits(horizontal_lines, vertical_lines)
        walls = self.recognize_walls2(horizontal_lines[:-2], vertical_lines[:-2])
        self.format_matrix_with_walls2(matrix, walls)
        level_str = get_level_str_from_matrix(matrix)
        return level_str


if __name__ == "__main__":
    analyzer = _Analyzer()
    # analyzer.take_snapshot()
    # analyzer.get_level_board_size_from_puzzle()
    analyzer.get_levels_str_from_puzzle()
