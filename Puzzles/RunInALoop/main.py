from typing import Self, override

from Puzzles.puzzle_analyzer import PuzzleAnalyzer, get_level_str_from_matrix

block_color = (170, 170, 170)

# Games 1 Puzzle Set 7
class _Analyzer(PuzzleAnalyzer):

    def __init__(self: Self):
        super().__init__(
            200,
            [(1, 5), (11, 6), (31, 7), (61, 8), (101, 9), (151, 10)]
        )

    def get_matrix_from_blocks(self: Self, blocks: set[tuple[int, int]]) -> list[list[str]]:
        result = []
        for row_idx in range(self.cell_count):
            row_result = []
            for col_idx in range(self.cell_count):
                ch = 'B' if (row_idx, col_idx) in blocks else ' '
                row_result.append(ch)
            result.append(row_result)
        return result


    @override
    def get_level_str_from_image(self: Self) -> str:
        horizontal_lines, vertical_lines = self.get_grid_lines_by_cell_count(self.cell_count)
        blocks = self.recognize_blocks(horizontal_lines, vertical_lines, lambda color: color[0] == 170)
        matrix = self.get_matrix_from_blocks(blocks)
        level_str = get_level_str_from_matrix(matrix)
        return level_str


if __name__ == "__main__":
    analyzer = _Analyzer()
    # analyzer.take_snapshot(2)
    # analyzer.get_level_board_size_from_puzzle()
    analyzer.get_levels_str_from_puzzle()
