from typing import Any

from .. import base_metric, score_result


class Contains(base_metric.BaseMetric):
    def __init__(
        self,
        searched_value: str,
        case_sensitive: bool = False,
        name: str = "ContainsMetric",
    ):
        super().__init__(name=name)

        self._case_sensitive = case_sensitive
        self._searched_value = (
            searched_value if case_sensitive else searched_value.lower()
        )

    def score(self, output: str, **ignored_kwargs: Any) -> score_result.ScoreResult:
        value = output if self._case_sensitive else output.lower()

        if self._searched_value in value:
            return score_result.ScoreResult(value=1.0, name=self.name)

        return score_result.ScoreResult(value=0.0, name=self.name)
