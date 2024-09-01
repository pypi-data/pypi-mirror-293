from typing import List


VERDICT_KEY = "context_precision_score"
REASON_KEY = "reason"


def generate_query(
    user_input: str, answer: str, expected_answer: str, contexts: List[str]
) -> str:
    return f"""
        YOU ARE AN EXPERT EVALUATOR SPECIALIZED IN ASSESSING THE "CONTEXT PRECISION" METRIC FOR LLM GENERATED OUTPUTS.
        YOUR TASK IS TO EVALUATE HOW PRECISELY A GIVEN ANSWER FROM AN LLM FITS THE EXPECTED ANSWER, GIVEN THE CONTEXT AND USER INPUT.

        ###INSTRUCTIONS###

        1. **EVALUATE THE CONTEXT PRECISION:**
            - **ANALYZE** the provided user input, expected answer, answer from another LLM, and the context.
            - **COMPARE** the answer from the other LLM with the expected answer, focusing on how well it aligns in terms of context, relevance, and accuracy.
            - **ASSIGN A SCORE** from 0.0 to 1.0 based on the following scale:

        ###SCALE FOR CONTEXT PRECISION METRIC (0.0 - 1.0)###

        - **0.0:** COMPLETELY INACCURATE – The LLM’s answer is entirely off-topic, irrelevant, or incorrect based on the context and expected answer.
        - **0.2:** MOSTLY INACCURATE – The answer contains significant errors, misunderstanding of the context, or is largely irrelevant.
        - **0.4:** PARTIALLY ACCURATE – Some correct elements are present, but the answer is incomplete or partially misaligned with the context and expected answer.
        - **0.6:** MOSTLY ACCURATE – The answer is generally correct and relevant but may contain minor errors or lack complete precision in aligning with the expected answer.
        - **0.8:** HIGHLY ACCURATE – The answer is very close to the expected answer, with only minor discrepancies that do not significantly impact the overall correctness.
        - **1.0:** PERFECTLY ACCURATE – The LLM’s answer matches the expected answer precisely, with full adherence to the context and no errors.

        2. **PROVIDE A REASON FOR THE SCORE:**
            - **JUSTIFY** why the specific score was given, considering the alignment with context, accuracy, relevance, and completeness.

        3. **RETURN THE RESULT IN A JSON FORMAT** as follows:
            - `"{VERDICT_KEY}"`: The score between 0.0 and 1.0.
            - `"{REASON_KEY}"`: A detailed explanation of why the score was assigned.

        ###WHAT NOT TO DO###
        - **DO NOT** assign a high score to answers that are off-topic or irrelevant, even if they contain some correct information.
        - **DO NOT** give a low score to an answer that is nearly correct but has minor errors or omissions; instead, accurately reflect its alignment with the context.
        - **DO NOT** omit the justification for the score; every score must be accompanied by a clear, reasoned explanation.
        - **DO NOT** disregard the importance of context when evaluating the precision of the answer.
        - **DO NOT** assign scores outside the 0.0 to 1.0 range.
        - **DO NOT** return any output format other than JSON.


        ###EXAMPLES###

        1. **Low ContextPrecision Example:**
            - **User Input:** "What is the capital of France?"
            - **Expected Answer:** "The capital of France is Paris."
            - **Answer from Other LLM:** "The capital of Italy is Rome."
            - **Context:** The user is asking about the capital city of a European country.
            - **Result:**
                ```json
                {{
                    "{VERDICT_KEY}": 0.0,
                    "{REASON_KEY}": "The answer provided by the LLM is completely inaccurate as it refers to the wrong country and does not address the user's question about France."
                }}
                ```

        2. **Medium ContextPrecision Example:**
            - **User Input:** "What is the capital of France?"
            - **Expected Answer:** "The capital of France is Paris."
            - **Answer from Other LLM:** "Paris is a city in Europe."
            - **Context:** The user is asking for the capital city of France.
            - **Result:**
                ```json
                {{
                    "{VERDICT_KEY}": 0.4,
                    "{REASON_KEY}": "While the answer mentions Paris, it fails to clearly identify it as the capital of France, thus providing only partial accuracy."
                }}
                ```

        3. **High ContextPrecision Example:**
            - **User Input:** "What is the capital of France?"
            - **Expected Answer:** "The capital of France is Paris."
            - **Answer from Other LLM:** "The capital of France is Paris."
            - **Context:** The user is asking about the capital city of France.
            - **Result:**
                ```json
                {{
                    "{VERDICT_KEY}": 1.0,
                    "{REASON_KEY}": "The answer perfectly matches the expected response, fully aligning with the context and providing the correct information."
                }}
                ```

        NOW, EVALUATE THE PROVIDED INPUTS AND CONTEXT TO DETERMINE THE CONTEXT PRECISION SCORE.

        ###INPUTS:###
        ***
        User input:
        {user_input}

        Answer:
        {answer}

        Expected Answer:
        {expected_answer}

        Contexts:
        {contexts}
        ***


    """
