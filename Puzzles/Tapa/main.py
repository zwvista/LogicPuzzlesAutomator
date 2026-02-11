from typing import Self, override

from Puzzles.tapa_base_analyzer import TapaBaseAnalyzer


class _Analyzer(TapaBaseAnalyzer):

    def __init__(self: Self):
        super().__init__(
            67,
            [(1,5), (4,6), (12,7), (20,8), (28,9), (36,10)]
        )

    @override
    def get_attr_str_from_image(self: Self) -> str:
        text = self.recognize_text(660, 56, 500, 34)
        return f' GameType="{text}"' if text else ''


if __name__ == "__main__":
    analyzer = _Analyzer()
    analyzer.get_levels_str_from_puzzle()
