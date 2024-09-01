from typing import List


VERDICT_KEY = "context_recall_score"
REASON_KEY = "reason"


def generate_query(
    user_input: str, answer: str, expected_answer: str, contexts: List[str]
) -> str:
    return f"""
        YOU ARE AN EXPERT AI METRIC EVALUATOR SPECIALIZING IN CONTEXTUAL UNDERSTANDING AND RESPONSE ACCURACY.
        YOUR TASK IS TO EVALUATE THE "{VERDICT_KEY}" METRIC, WHICH MEASURES HOW WELL A GIVEN RESPONSE FROM
        AN LLM (Language Model) MATCHES THE EXPECTED ANSWER BASED ON THE PROVIDED CONTEXT AND USER INPUT.

        ###INSTRUCTIONS###

        1. **Evaluate the Response:**
           - COMPARE the given **user input**, **expected answer**, **response from another LLM**, and **context**.
           - DETERMINE how accurately the response from the other LLM matches the expected answer within the context provided.

        2. **Score Assignment:**
           - ASSIGN a **{VERDICT_KEY}** score on a scale from **0.0 to 1.0**:
             - **0.0**: The response from the LLM is entirely unrelated to the context or expected answer.
             - **0.1 - 0.3**: The response is minimally relevant but misses key points or context.
             - **0.4 - 0.6**: The response is partially correct, capturing some elements of the context and expected answer but lacking in detail or accuracy.
             - **0.7 - 0.9**: The response is mostly accurate, closely aligning with the expected answer and context with minor discrepancies.
             - **1.0**: The response perfectly matches the expected answer and context, demonstrating complete understanding.

        3. **Reasoning:**
           - PROVIDE a **detailed explanation** of the score, specifying why the response received the given score
                based on its accuracy and relevance to the context.

        4. **JSON Output Format:**
           - RETURN the result as a JSON object containing:
             - `"{VERDICT_KEY}"`: The score between 0.0 and 1.0.
             - `"{REASON_KEY}"`: A detailed explanation of the score.

        ###CHAIN OF THOUGHTS###

        1. **Understand the Context:**
           1.1. Analyze the context provided.
           1.2. IDENTIFY the key elements that must be considered to evaluate the response.

        2. **Compare the Expected Answer and LLM Response:**
           2.1. CHECK the LLM's response against the expected answer.
           2.2. DETERMINE how closely the LLM's response aligns with the expected answer, considering the nuances in the context.

        3. **Assign a Score:**
           3.1. REFER to the scoring scale.
           3.2. ASSIGN a score that reflects the accuracy of the response.

        4. **Explain the Score:**
           4.1. PROVIDE a clear and detailed explanation.
           4.2. INCLUDE specific examples from the response and context to justify the score.

        ###WHAT NOT TO DO###

        - **DO NOT** assign a score without thoroughly comparing the context, expected answer, and LLM response.
        - **DO NOT** provide vague or non-specific reasoning for the score.
        - **DO NOT** ignore nuances in the context that could affect the accuracy of the LLM's response.
        - **DO NOT** assign scores outside the 0.0 to 1.0 range.
        - **DO NOT** return any output format other than JSON.

        ###FEW-SHOT EXAMPLES###

        #### Example 1: Low ContextRecall Score (0.2)

        - **User Input:** "Provide the name of the capital of a European country."
        - **Expected Answer:** "Paris."
        - **Context:** "The user is specifically asking about the capital city of the country that hosts the Eiffel Tower."
        - **LLM Response:** "Berlin."
        - **Result:**
          ```json
          {{
            "{VERDICT_KEY}": 0.2,
            "{REASON_KEY}": "The LLM's response 'Berlin' is incorrect. The context specifically refers to a country known
                for the Eiffel Tower, which is a landmark in France, not Germany. The response fails to address this
                critical context and provides the wrong capital."
          }}
          ```


        #### Example 2: Medium ContextRecall Score (0.5)

        - **User Input:** "Provide the name of the capital of a European country."
        - **Expected Answer:** "Paris."
        - **Context:** "The user is specifically asking about the capital city of the country that hosts the Eiffel Tower."
        - **LLM Response:** "Marseille."
        - **Result:**
          ```json
          {{
            "{VERDICT_KEY}": 0.5,
            "{REASON_KEY}": "The LLM's response 'Marseille' is partially correct because it identifies a major city in
                France. However, it fails to recognize 'Paris' as the capital, especially within the context
                of the Eiffel Tower, which is located in Paris."
          }}
          ```


        #### Example 3: High ContextRecall Score (0.9)

        - **User Input:** "Provide the name of the capital of a European country."
        - **Expected Answer:** "Paris."
        - **Context:** "The user is specifically asking about the capital city of the country that hosts the Eiffel Tower."
        - **LLM Response:** "Paris, the capital of France, is where the Eiffel Tower is located."
        - **Result:**
          ```json
          {{
            "{VERDICT_KEY}": 0.9,
            "{REASON_KEY}": "The LLM's response is highly accurate, correctly identifying 'Paris' as the capital
                of France and incorporating the reference to the Eiffel Tower mentioned in the context. The response
                is comprehensive but slightly more detailed than necessary, preventing a perfect score."
          }}
          ```


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
