from typing import Self

from Puzzles.tapa_base_analyzer import TapaBaseAnalyzer


class _Analyzer(TapaBaseAnalyzer):

    def __init__(self: Self):
        super().__init__(
            42,
            [(1, 5), (7, 6), (13, 7), (19, 8), (25, 9), (31, 10)]
        )


if __name__ == "__main__":
    analyzer = _Analyzer()
    # analyzer.take_snapshot()
    # analyzer.get_level_board_size_from_puzzle()
    analyzer.get_levels_str_from_puzzle()
