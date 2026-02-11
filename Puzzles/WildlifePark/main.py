from typing import Self, override

from Puzzles.puzzle_analyzer import PuzzleAnalyzer, get_template_img_4channel_list, get_level_str_from_matrix


class _Analyzer(PuzzleAnalyzer):
    ANIMALS_PATH = [
        '../../images/bull.png',
        '../../images/camel.png',
        '../../images/chick.png',
        '../../images/crab.png',
        '../../images/elephant.png',
        '../../images/fox.png',
        '../../images/giraffe.png',
        '../../images/hedgehog.png',
        '../../images/hippopotamus.png',
        '../../images/kangaroo.png',
        '../../images/koala.png',
        '../../images/lemur.png',
        '../../images/lion.png',
        '../../images/monkey.png',
        '../../images/squirrel.png',
        '../../images/swan.png',
        '../../images/toucan.png',
        '../../images/turtle.png',
        '../../images/tiger.png',
        '../../images/whale.png',
        '../../images/zebra.png',
    ]
    template_img_4channel_list = get_template_img_4channel_list(*ANIMALS_PATH)

    def __init__(self: Self):
        super().__init__(
            200,
            [(1, 5), (11, 6), (41, 7), (71, 8), (111, 9), (151, 10)]
        )

    def recognize_template(
            self: Self,
            horizontal_line_list: list[tuple[int, int]],
            vertical_line_list: list[tuple[int, int]]
    ) -> list[list[str]]:
        def has_dot(x: int, y: int) -> bool:
            for dx in range(0, 2):
                for dy in range(0, 2):
                    b, g, r = self.large_img_bgr[y + dy, x + dx]
                    if b == 255 and g == 255 and r == 255:
                        return True
            return False

        result = []
        indexes = []

        for row_idx, (y, h) in enumerate(vertical_line_list):
            row_result = []
            for col_idx, (x, w) in enumerate(horizontal_line_list):
                row_result.append('x' if has_dot(x, y) else ' ')
                row_result.append(' ' if row_idx > 0 else '-')
            row_result.append('x' if has_dot(x + w, y) else ' ')
            result.append(row_result)

            row_result = ['|']
            for col_idx, (x, w) in enumerate(horizontal_line_list):
                horizontal_line_results = self.analyze_horizontal_line(y_coord=y + h // 2, start_x=x + 10, end_x=x+w - 10)
                if len(horizontal_line_results) == 1:
                    index = -1
                else:
                    index = self.get_template_index_by_diff_in_region(
                        template_img_4channel_list=self.template_img_4channel_list,
                        top_left_coord=(x, y),
                        size=(w, h),
                    )
                if index == -1:
                    ch = ' '
                else:
                    if index not in indexes:
                        indexes.append(index)
                    ch = chr(ord('A') + indexes.index(index))
                if col_idx > 0:
                    row_result.append(' ')
                row_result.append(ch)
            row_result.append('|')
            result.append(row_result)

        row_result = []
        for col_idx, (x, w) in enumerate(horizontal_line_list):
            row_result.append('x' if has_dot(x, y + h) else ' ')
            row_result.append('-')
        row_result.append('x' if has_dot(x + w, y + h) else ' ')
        result.append(row_result)

        return result

    @override
    def get_level_str_from_image(self: Self) -> str:
        horizontal_lines, vertical_lines = self.get_grid_lines_by_cell_count(self.cell_count)
        matrix = self.recognize_template(horizontal_lines, vertical_lines)
        level_str = get_level_str_from_matrix(matrix)
        return level_str


if __name__ == "__main__":
    analyzer = _Analyzer()
    # analyzer.take_snapshot(app_series_no=2)
    # analyzer.get_level_board_size_from_puzzle()
    analyzer.get_levels_str_from_puzzle()
