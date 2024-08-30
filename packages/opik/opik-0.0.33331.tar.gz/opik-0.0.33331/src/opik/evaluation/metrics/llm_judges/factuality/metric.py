import json
import logging
import pprint
from typing import Union, Optional, List, Any

from opik.evaluation.models import base_model, models_factory
from opik.evaluation.metrics import score_result, base_metric
from opik import logging_messages

from . import template


LOGGER = logging.getLogger(__name__)


class Factuality(base_metric.BaseMetric):
    def __init__(
        self,
        model: Optional[Union[str, base_model.CometBaseModel]] = None,
        name: str = "FactualityMetric",
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
            list_content = json.loads(content)

            reason = ""
            score = 0.0

            for claim in list_content:
                pprint.pprint(claim)
                verdict = claim["verdict"]
                reason += claim["reason"] + "\n"

                if verdict == template.VERDICT_TRUTH:
                    score += 1.0
                elif verdict == template.VERDICT_LIE:
                    score += 0.0
                elif verdict == template.VERDICT_UNCLEAR:
                    score += 0.5

            score /= len(list_content)

            return score_result.ScoreResult(name=self.name, value=score, reason=reason)
        except Exception:
            LOGGER.warning(logging_messages.FACTUALITY_SCORE_CALC_FAILED, exc_info=True)
            return score_result.ScoreResult(
                name=self.name,
                value=0,
                scoring_failed=True,
                reason=logging_messages.FACTUALITY_SCORE_CALC_FAILED,
            )
