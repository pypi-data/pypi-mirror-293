import re
from typing import Any, Union

from .. import base_metric, score_result


class RegexMatch(base_metric.BaseMetric):
    def __init__(
        self,
        regex: Union[str, re.Pattern],
        name: str = "RegexMatchMetric",
    ):
        super().__init__(name=name)

        if isinstance(regex, str):
            regex = re.compile(regex)

        self._regex_pattern: re.Pattern = regex

    def score(self, output: str, **ignored_kwargs: Any) -> score_result.ScoreResult:
        if self._regex_pattern.match(output):
            return score_result.ScoreResult(value=1.0, name=self.name)

        return score_result.ScoreResult(value=0.0, name=self.name)
