# core/experiments.py

import pandas as pd
import logging
import textwrap
import json
import re

# ==============================================================================
# THIS IS THE SACRED, UNALTERED CORE LOGIC OF THE EXPERIMENTS
#
# PRIME DIRECTIVE: The internal logic and variable names within these functions
# are a direct, faithful copy of the original script and must not be changed.
# The functions have been structured to accept dependencies and return results,
# but the core experimental loops remain sacrosanct.
# ==============================================================================

def run_text_generation_experiment(
    models_to_test: dict,
    hf_handlers: dict,
    groq_generate_func,
    judge_model_id: str,
    traits_definitions: dict,
    questions: list
) -> pd.DataFrame:
    """
    Executes the main text generation and judging experiment.

    This function contains the unaltered core logic from Part 4 of the original script.

    Args:
        models_to_test (dict): Configuration for the models being tested.
        hf_handlers (dict): Pre-initialized Hugging Face model handlers.
        groq_generate_func: The function to call for Groq API generation.
        judge_model_id (str): The ID of the model used for judging.
        traits_definitions (dict): The definitions for personality traits.
        questions (list): The list of questions to ask the models.

    Returns:
        pd.DataFrame: A DataFrame containing the detailed results of the experiment.
    """
    logging.info("🚀 Starting Main Text Generation Experiment...")
    results_list = []
    
    # --- Start of Unaltered Core Logic Block 1 ---
    total_generations = len(models_to_test) * len(traits_definitions["generation"]) * 5 * len(questions)
    current_generation = 0
    print(f"🚀 Starting main experiment. Total generations to perform: {total_generations}")

    for model_key, model_info in models_to_test.items():
        print("-" * 70); logging.info(f"--- Testing Model: {model_key} ---"); print(f"--- Testing Model: {model_key} ---"); print("-" * 70)
        for trait_key, trait_gen_info in traits_definitions["generation"].items():
            trait_name = trait_gen_info["name"]
            for trait_score_num in range(1, 6):
                for question in questions:
                    current_generation += 1; print(f"[{current_generation}/{total_generations}] Generating for {model_key}, {trait_name}, Score {trait_score_num}...")
                    system_prompt_generate = textwrap.dedent(f"""TASK: Answer the QUESTION according to your PERSONALITY. Use INSTRUCTION. Use at most 5 sentences. Do not mention your personality traits in the text. Type only the answer, without the information about your personality score. PERSONALITY: - Your personality trait "{trait_name}" is rated as {trait_score_num}. INSTRUCTION: - The personality trait is rated from 1 to 5. 1 is the lowest score and 5 is the highest score. - {trait_gen_info['low']} - {trait_gen_info['high']}""")
                    user_prompt_generate = f"QUESTION:\n```\n{question}\n```"
                    
                    if model_info["handler"] == "groq": generated_text, status = groq_generate_func(model_info["model_id"], system_prompt_generate, user_prompt_generate)
                    elif model_info["handler"] == "hf": handler = hf_handlers[model_key]; generated_text, status = handler.generate_response(system_prompt_generate, user_prompt_generate)
                    
                    if status == 'fail': logging.warning(f"Failed to generate text for {model_key} on question: {question}"); continue

                    trait_class_info = traits_definitions["classification"][trait_key]
                    system_prompt_judge = textwrap.dedent(f"""You will be provided with answers to questions. Detect the score of {trait_name} for the author of the INPUT from the list [-2, -1, 0, 1, 2] or Nondistinguishable. Use INSTRUCTION. TASK: 1. First, list CLUES (i.e., keywords, phrases, contextual information, semantic relations, semantic meaning, tones, references) that support the score determination of {trait_name} of INPUT. 2. Second, deduce the diagnostic REASONING process from premises (i.e., clues, input) that supports the INPUT score determination (Limit the number of words to 130). 3. Third, based on clues, reasoning and input, determine the score of {trait_name} for the author of INPUT from the list [-2, -1, 0, 1, 2] or Nondistinguishable. 4. Mark what made you choose this score as decision type: Explicit signs, Implicit signs, Intuition, Nondistinguishable. 5. Provide your output in JSON format with the keys: score, clues, reasoning, decision type. PROVIDE ONLY JSON. INSTRUCTION: - Definition: {trait_class_info.get('definition', '')} - High score of {trait_name} (maximum 2): '{trait_class_info['high']}' - Low score of {trait_name} (minimum -2): '{trait_class_info['low']}' - Explicit signs: The person mentions obvious facts that are connected with this trait score. - Implicit signs: The person mentions facts that may imply them having this trait score. - Intuition: My intuition tells that the person has this trait score. - Nondistinguishable: I can't tell what trait score the person has. - If the text does not contain substantial, significant, and convincing indicators of the trait score, then use Nondistinguishable. - Choose something other than Nondistinguishable if you have a high degree of confidence in the answer.""")
                    user_prompt_judge = f"Question: {question} INPUT: {generated_text}"
                    
                    judge_response_raw, judge_status = groq_generate_func(judge_model_id, system_prompt_judge, user_prompt_judge, temperature=0.0)
                    if judge_status == 'fail': logging.warning(f"Judge model failed to evaluate text from {model_key}"); continue

                    judge_result = {}
                    try:
                        match = re.search(r'\{.*\}', judge_response_raw, re.DOTALL);
                        if match: json_string = match.group(0); judge_result = json.loads(json_string)
                        else: raise ValueError("No JSON found")
                    except Exception as e:
                        logging.error(f"Could not parse JSON from judge: {e}\nRaw response: {judge_response_raw}"); judge_result = {'score': None, 'clues': None, 'reasoning': 'JSON PARSE ERROR', 'decision type': None}

                    results_list.append({'model_key': model_key, 'model_id': model_info["model_id"], 'prompted_trait': trait_name, 'prompted_score': trait_score_num, 'question': question, 'generated_text': generated_text, 'judge_score': judge_result.get('score'), 'judge_clues': judge_result.get('clues'), 'judge_reasoning': judge_result.get('reasoning'), 'judge_decision_type': judge_result.get('decision type')})
    # --- End of Unaltered Core Logic Block 1 ---

    logging.info("✅ Main Experiment complete!")
    return pd.DataFrame(results_list)


def run_questionnaire_experiment(
    models_to_test: dict,
    hf_handlers: dict,
    groq_generate_func,
    bfi44_questions: dict,
    bfi44_scores_dict: dict,
    traits_definitions: dict
) -> pd.DataFrame:
    """
    Executes the BFI-44 questionnaire-based experiment.

    This function contains the unaltered core logic from Part 5 of the original script.

    Args:
        models_to_test (dict): Configuration for the models being tested.
        hf_handlers (dict): Pre-initialized Hugging Face model handlers.
        groq_generate_func: The function to call for Groq API generation.
        bfi44_questions (dict): The BFI-44 questions.
        bfi44_scores_dict (dict): The scoring dictionary for BFI-44 responses.
        traits_definitions (dict): The definitions for personality traits.

    Returns:
        pd.DataFrame: A DataFrame containing the detailed results of the experiment.
    """
    logging.info("🚀 Starting Questionnaire Experiment...")
    questionnaire_results_list = []

    # --- Start of Unaltered Core Logic Block 2 ---
    total_q_generations = len(models_to_test) * len(bfi44_questions) * 2
    current_q_generation = 0

    for model_key, model_info in models_to_test.items():
        for trait_key_long, questions in bfi44_questions.items():
            trait_key_short = trait_key_long[0].upper(); trait_info = traits_definitions['generation'][trait_key_short]; trait_name = trait_info['name']
            for level in ['high', 'low']:
                current_q_generation += 1; print(f"[{current_q_generation}/{total_q_generations}] Running Questionnaire for {model_key} on {trait_name} ({level})...")
                trait_prompt = f"Act as a person with a {level} score in {trait_name}. {trait_info[level]}"
                provided_options = '\n'.join(f"- {option}" for option in bfi44_scores_dict.keys()); constant_list = list(bfi44_scores_dict.keys())
                system_prompt = textwrap.dedent(f"""TASK: Indicate your level of agreement or disagreement with the statement in the CHARACTERISTICS according to your PERSONALITY. Use only the PROVIDED OPTIONS. PERSONALITY: ``` {trait_prompt} ``` PROVIDED OPTIONS: {provided_options} Provide your output only from the constant list {constant_list} without explanation.""")

                for question_set in questions:
                    user_prompt = f"CHARACTERISTICS:\n```\n{question_set['q_statement']}\n```"
                    if model_info["handler"] == "groq": answer, status = groq_generate_func(model_info["model_id"], system_prompt, user_prompt, temperature=0.7)
                    elif model_info["handler"] == "hf": handler = hf_handlers[model_key]; answer, status = handler.generate_response(system_prompt, user_prompt)
                    if status == 'ok': questionnaire_results_list.append({'model_key': model_key, 'trait': trait_name, 'prompted_level': level, 'Q_type': question_set['q_type'], 'Answer': answer})
    # --- End of Unaltered Core Logic Block 2 ---

    logging.info("✅ Questionnaire Experiment complete!")
    return pd.DataFrame(questionnaire_results_list)
