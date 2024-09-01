from typing import Any

import Levenshtein

from .. import base_metric, score_result


class LevenshteinRatio(base_metric.BaseMetric):
    """
    Calculates the Levenshtein ratio between two strings.
    """

    def __init__(
        self,
        searched_value: str,
        case_sensitive: bool = False,
        name: str = "LevenshteinRatioMetric",
    ):
        super().__init__(name=name)

        self._case_sensitive = case_sensitive
        self._searched_value = (
            searched_value if case_sensitive else searched_value.lower()
        )

    def score(self, output: str, **ignored_kwargs: Any) -> score_result.ScoreResult:
        value = output if self._case_sensitive else output.lower()

        score = Levenshtein.ratio(value, self._searched_value)

        return score_result.ScoreResult(value=score, name=self.name)
