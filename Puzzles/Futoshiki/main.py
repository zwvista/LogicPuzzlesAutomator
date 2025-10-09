from typing import Self, override

from Puzzles.puzzle_analyzer import PuzzleAnalyzer, get_template_img_4channel_list, process_pixel_long_results, \
    get_level_str_from_matrix


# Puzzle Set 2
class _Analyzer(PuzzleAnalyzer):

    UP_PATH = '../../images/TileContent/navigate_up.png'
    DOWN_PATH = '../../images/TileContent/navigate_down.png'
    LEFT_PATH = '../../images/TileContent/navigate_left.png'
    RIGHT_PATH = '../../images/TileContent/navigate_right.png'
    MINUS_PATH = '../../images/TileContent/navigate_minus.png'
    PIPE_PATH = '../../images/TileContent/navigate_pipe.png'
    template_img_4channel_list_row = get_template_img_4channel_list(UP_PATH, DOWN_PATH, MINUS_PATH)
    template_img_4channel_list_col = get_template_img_4channel_list(LEFT_PATH, RIGHT_PATH, PIPE_PATH)

    def __init__(self: Self):
        super().__init__(
            190,
            [(1,4), (10,5), (43,6), (81,7), (111,8), (161,9)],
            True
        )

    def recognize_template_and_digits(
            self: Self,
            horizontal_line_list: list[tuple[int, int]],
            vertical_line_list: list[tuple[int, int]]
    ) -> list[list[str]]:
        result = []
        for row_idx, (y, h) in enumerate(vertical_line_list):
            row_result = []
            is_op_row = row_idx % 2 == 1
            for col_idx, (x, w) in enumerate(horizontal_line_list):
                is_op_col = col_idx % 2 == 1
                if not is_op_row and not is_op_col:
                    ch = self.recognize_digit(x, y, w, h) or ' '
                elif is_op_row and is_op_col:
                    ch = ' '
                elif is_op_row:
                    horizontal_line_results = self.analyze_horizontal_line(y_coord=y + h // 2, start_x=x, end_x=x+w)
                    processed_horizontal_lines = process_pixel_long_results(horizontal_line_results, is_horizontal=True)
                    if len(processed_horizontal_lines) == 1:
                        index = -1
                    else:
                        h2 = w2 = h // 2 * 2
                        x2 = x + w // 2 - w2 // 2
                        y2 = y + h // 2 - h2 // 2
                        index = self.get_template_index_by_diff_in_region(
                            template_img_4channel_list=self.template_img_4channel_list_row,
                            top_left_coord=(x2, y2),
                            size=(w2, h2),
                        )
                    ch = ' ' if index == -1 else '^v-'[index]
                else: # is_op_col
                    vertical_line_results = self.analyze_vertical_line(x_coord=x + w // 2, start_y=y, end_y=y+h)
                    processed_vertical_lines = process_pixel_long_results(vertical_line_results, is_horizontal=False)
                    if len(processed_vertical_lines) == 1:
                        index = -1
                    else:
                        h2 = w2 = w // 2 * 2
                        x2 = x + w // 2 - w2 // 2
                        y2 = y + h // 2 - h2 // 2
                        index = self.get_template_index_by_diff_in_region(
                            template_img_4channel_list=self.template_img_4channel_list_col,
                            top_left_coord=(x2, y2),
                            size=(w2, h2),
                        )
                    ch = ' ' if index == -1 else '<>|'[index]
                row_result.append(ch)
            result.append(row_result)
        return result

    @override
    def get_level_str_from_image(self: Self) -> str:
        horizontal_line_results = self.analyze_horizontal_line(y_coord=210, start_x=0, end_x=1180)
        processed_horizontal_lines = process_pixel_long_results(horizontal_line_results, is_horizontal=True, threshold=40)
        vertical_line_results = self.analyze_vertical_line(x_coord=10, start_y=200, end_y=1380)
        processed_vertical_lines = process_pixel_long_results(vertical_line_results, is_horizontal=False, threshold=40)
        matrix = self.recognize_template(processed_horizontal_lines, processed_vertical_lines)
        level_str = get_level_str_from_matrix(matrix)
        return level_str


analyzer = _Analyzer()
analyzer.get_levels_str_from_puzzle()
