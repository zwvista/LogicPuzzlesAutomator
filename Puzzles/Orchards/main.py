from typing import Self

from Puzzles.Parks.main import ParksBaseAnalyzer


class _Analyzer(ParksBaseAnalyzer):

    def __init__(self: Self):
        super().__init__(
            88,
            [(1,6), (11,7), (31,8), (51,9), (71,10), (86,11)],
        )

if __name__ == "__main__":
    analyzer = _Analyzer()
    # analyzer.take_snapshot()
    analyzer.get_levels_str_from_puzzle()

# Level 37 is incorrect
