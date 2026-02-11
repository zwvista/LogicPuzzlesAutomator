from typing import Self

from Puzzles.Parks.main import ParksBaseAnalyzer


class _Analyzer(ParksBaseAnalyzer):

    def __init__(self: Self):
        super().__init__(
            21,
            [(1,5), (4,6), (7,7), (10,8), (13,9), (16,10)],
        )

if __name__ == "__main__":
    analyzer = _Analyzer()
    # analyzer.take_snapshot()
    analyzer.get_levels_str_from_puzzle()
