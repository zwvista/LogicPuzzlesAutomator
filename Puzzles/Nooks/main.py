from typing import Self, override

import cv2

from Puzzles.puzzle_analyzer import PuzzleAnalyzer, get_level_str_from_matrix, to_base_36


class _Analyzer(PuzzleAnalyzer):

    QM_PATH = '../../images/qm.png'
    template_img_4channel = cv2.imread(QM_PATH, cv2.IMREAD_UNCHANGED)

    def __init__(self: Self):
        super().__init__(
            200,
            [(1,4), (6,5), (31,6), (71,7), (111,8), (141,9), (171,10)]
        )

    @override
    def recognize_digits(
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
                    text = ' '
                else:
                    diff = self.get_template_diff_in_region(
                        template_img_4channel=self.template_img_4channel,
                        top_left_coord=(x+5, y+5),
                        size=(w-10, h-10),
                    )
                    # print(f'{row_idx=}, {col_idx=}, {diff=}')
                    if diff < .7:
                        text = '?'
                    else:
                        roi = self.large_img_rgb[y:y + h, x:x + w]
                        scale = .5 if w > 220 else 1 if w > 180 else 2 if w > 150 else 3 if w > 120 else 4
                        roi_large = cv2.resize(roi, None, fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)
                        output = self.reader.readtext(roi_large, allowlist="0123456789")
                        if not output:
                            text = "7"
                        else:
                            _, text, prob = output[0]
                            text = '2' if text == "22" else text
                row_result.append(to_base_36(text))
            result.append(row_result)
        return result

    @override
    def get_level_str_from_image(self: Self) -> str:
        horizontal_lines, vertical_lines = self.get_grid_lines_by_cell_count(self.cell_count)

        gray = cv2.cvtColor(self.large_img_bgr, cv2.COLOR_BGR2GRAY)
        _, self.large_img_bgr = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)
        self.large_img_bgr = cv2.cvtColor(self.large_img_bgr, cv2.COLOR_GRAY2BGR)
        self.large_img_rgb = cv2.cvtColor(self.large_img_bgr, cv2.COLOR_BGR2RGB)
        # cv2.imshow("Grid Intersections", self.large_img_rgb)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

        matrix = self.recognize_digits(horizontal_lines, vertical_lines)
        level_str = get_level_str_from_matrix(matrix)
        return level_str


if __name__ == "__main__":
    analyzer = _Analyzer()
    # analyzer.take_snapshot()
    analyzer.get_levels_str_from_puzzle()
