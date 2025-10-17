from typing import Self

from Puzzles.tapa_base_analyzer import TapaBaseAnalyzer


# Games 1 Puzzle Set 10
class _Analyzer(TapaBaseAnalyzer):

    def __init__(self: Self):
        super().__init__(
            56,
            [(1, 6), (17, 8), (37, 10), (49, 12)]
        )


if __name__ == "__main__":
    analyzer = _Analyzer()
    # analyzer.take_snapshot()
    # analyzer.get_level_board_size_from_puzzle()
    analyzer.get_levels_str_from_puzzle()
