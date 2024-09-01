import json
import logging
from typing import Any, List, Optional, Union

from opik import logging_messages
from opik.evaluation.metrics import base_metric, score_result
from opik.evaluation.models import base_model, models_factory
from . import template

LOGGER = logging.getLogger(__name__)


class AnswerRelevance(base_metric.BaseMetric):
    def __init__(
        self,
        model: Optional[Union[str, base_model.CometBaseModel]] = None,
        name: str = "AnswerRelevanceMetric",
    ):
        super().__init__(
            name=name,
        )

        self._init_model(model)

    def _init_model(
        self, model: Optional[Union[str, base_model.CometBaseModel]]
    ) -> None:
        if isinstance(model, base_model.CometBaseModel):
            self._model = model
        else:
            self._model = models_factory.get(model_name=model)

    def score(
        self, input: str, output: str, context: List[str], **ignored_kwargs: Any
    ) -> score_result.ScoreResult:
        llm_query = template.generate_query(
            user_input=input, answer=output, contexts=context
        )
        model_output = self._model.generate(input=llm_query)

        return self._parse_model_output(model_output)

    async def ascore(
        self, input: str, output: str, context: List[str], **ignored_kwargs: Any
    ) -> score_result.ScoreResult:
        llm_query = template.generate_query(
            user_input=input, answer=output, contexts=context
        )
        model_output = await self._model.agenerate(input=llm_query)

        return self._parse_model_output(model_output)

    def _parse_model_output(self, content: str) -> score_result.ScoreResult:
        try:
            dict_content = json.loads(content)
            score: float = dict_content[template.VERDICT_KEY]

            if not (0.0 <= score <= 1.0):
                score = 0.5

            return score_result.ScoreResult(
                name=self.name, value=score, reason=dict_content[template.REASON_KEY]
            )
        except Exception:
            LOGGER.warning(
                logging_messages.ANSWER_RELEVANCE_SCORE_CALC_FAILED, exc_info=True
            )
            return score_result.ScoreResult(
                name=self.name,
                value=0,
                scoring_failed=True,
                reason=logging_messages.ANSWER_RELEVANCE_SCORE_CALC_FAILED,
            )
