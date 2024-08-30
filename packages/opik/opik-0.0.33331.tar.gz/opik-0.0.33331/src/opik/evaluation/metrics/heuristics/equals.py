from typing import Any

from .. import base_metric, score_result


class Equals(base_metric.BaseMetric):
    def __init__(
        self,
        case_sensitive: bool = False,
        name: str = "EqualsMetric",
    ):
        super().__init__(name=name)
        self._case_sensitive = case_sensitive

    def score(
        self, output: str, expected_output: str, **ignored_kwargs: Any
    ) -> score_result.ScoreResult:
        value_left = output if self._case_sensitive else output.lower()
        value_right = (
            expected_output if self._case_sensitive else expected_output.lower()
        )

        if value_left == value_right:
            return score_result.ScoreResult(value=1.0, name=self.name)

        return score_result.ScoreResult(value=0.0, name=self.name)
