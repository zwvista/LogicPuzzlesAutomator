from typing import Self

from Puzzles.tapa_base_analyzer import TapaBaseAnalyzer


# Games 1 Puzzle Set 9
class _Analyzer(TapaBaseAnalyzer):

    def __init__(self: Self):
        super().__init__(
            40,
            [(1, 5), (9, 6), (19, 7), (29, 8)]
        )


if __name__ == "__main__":
    analyzer = _Analyzer()
    # analyzer.take_snapshot()
    # analyzer.get_level_board_size_from_puzzle()
    analyzer.get_levels_str_from_puzzle()
