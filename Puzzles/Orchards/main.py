from typing import Self

from Puzzles.Parks.main import ParksLikeAnalyzer


# Games 1 Puzzle Set 11
class _Analyzer(ParksLikeAnalyzer):

    def __init__(self: Self):
        super().__init__(
            88,
            [(1,6), (11,7), (31,8), (51,9), (71,10), (86,11)],
        )

analyzer = _Analyzer()
# analyzer.take_snapshot()
analyzer.get_levels_str_from_puzzle()

# Level 37 is incorrect
