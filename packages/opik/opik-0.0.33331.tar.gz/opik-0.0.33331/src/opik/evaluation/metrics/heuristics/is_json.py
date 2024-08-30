import json
from typing import Any

from .. import base_metric, score_result


class IsJson(base_metric.BaseMetric):
    def __init__(self, name: str = "IsJsonMetric") -> None:
        super().__init__(name)

    def score(self, output: str, **ignored_kwargs: Any) -> score_result.ScoreResult:
        try:
            json.loads(output)
            return score_result.ScoreResult(value=1.0, name=self.name)
        except Exception:
            return score_result.ScoreResult(value=0.0, name=self.name)
