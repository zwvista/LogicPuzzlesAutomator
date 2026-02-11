from typing import Self

from Puzzles.tapa_base_analyzer import TapaBaseAnalyzer


class _Analyzer(TapaBaseAnalyzer):

    def __init__(self: Self):
        super().__init__(
            39,
            [(1, 5), (7, 6), (13, 7), (16, 8), (19, 9), (25, 10), (26, 8), (28, 10), (29, 8), (34, 9)]
        )


if __name__ == "__main__":
    analyzer = _Analyzer()
    # analyzer.take_snapshot()
    # analyzer.get_level_board_size_from_puzzle()
    analyzer.get_levels_str_from_puzzle(7, 12)
