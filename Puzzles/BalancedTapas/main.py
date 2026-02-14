from typing import Self, override

from Puzzles.tapa_base_analyzer import TapaBaseAnalyzer


class _Analyzer(TapaBaseAnalyzer):

    def __init__(self: Self):
        super().__init__(
            61,
            [(1, 5), (7, 6), (19, 7), (29, 8), (35, 9), (43, 10), (51, 11), (59, 12)]
        )

    @override
    def get_attr_str_from_image(self: Self) -> str:
        horizontal_line_results = self.analyze_horizontal_line(210, 20, 1170)
        pt = next((o for o in horizontal_line_results if 200 < o.color[1] < 210), None)
        n = pt.position[0] / self.cell_length
        s = f'{n:.1f}'
        s = s.replace('.0', '')
        return f' LeftPart="{s}"'

if __name__ == "__main__":
    analyzer = _Analyzer()
    # analyzer.take_snapshot()
    # analyzer.get_level_board_size_from_puzzle()
    analyzer.get_levels_str_from_puzzle()
