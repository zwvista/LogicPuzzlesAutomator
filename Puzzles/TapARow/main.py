from typing import Self

from Puzzles.tapa_base_analyzer import TapaBaseAnalyzer


# Games 1 Puzzle Set 9
class _Analyzer(TapaBaseAnalyzer):

    def __init__(self: Self):
        super().__init__(
            50,
            [(1, 5), (7, 6), (17, 7), (25, 8), (35, 9), (47, 10)]
        )


if __name__ == "__main__":
    analyzer = _Analyzer()
    # analyzer.take_snapshot()
    # analyzer.get_level_board_size_from_puzzle()
    analyzer.get_levels_str_from_puzzle(1, 6)
