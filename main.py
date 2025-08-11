# main.py

import logging
import pandas as pd

# --- Configuration Imports ---
# Import all settings and prompt data from the config module.
from config import settings
from config import prompts

# --- Model Handler Imports ---
# Import the specific functions and classes for model interaction.
from models.handlers import HuggingFaceModelHandler, generate_response_groq

# --- Core Experiment Imports ---
# Import the sacred, unaltered experiment functions.
from core.experiments import run_text_generation_experiment, run_questionnaire_experiment

# --- Analysis Imports ---
# Import all analysis and plotting functions.
from analysis.plotting import plot_confusion_matrices, plot_questionnaire_histograms
from analysis.similarity import analyze_and_save_similarity_data, plot_similarity_heatmaps

# --- Utility Imports ---
# Import helper functions for tasks like saving files.
from utils.helpers import save_dataframe_to_csv, ensure_dir_exists

def main():
    """
    The main entry point for the entire project.
    This function orchestrates the setup, execution, analysis, and saving of results.
    """
    # 1. --- SETUP ---
    # Configure basic logging to see the progress of the script.
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    print("="*80)
    logging.info("STARTING PERSONALITY ASSESSMENT SUITE")
    print("="*80)

    # Create the main results directory where all outputs will be saved.
    ensure_dir_exists(settings.RESULTS_DIR)

    # 2. --- MODEL INITIALIZATION ---
    # Pre-load all specified Hugging Face models to avoid loading them repeatedly.
    hf_handlers = {}
    for model_key, model_info in settings.MODELS_TO_TEST.items():
        if model_info["handler"] == "hf":
            try:
                logging.info(f"Pre-loading Hugging Face model: {model_key}...")
                hf_handlers[model_key] = HuggingFaceModelHandler(model_info["model_id"])
            except Exception as e:
                logging.critical(f"Fatal error loading model {model_key}. Aborting. Error: {e}")
                return # Exit if a critical model can't be loaded.

    # 3. --- EXECUTE EXPERIMENTS ---
    # Run the two core experiments to get the raw data.
    
    # Run the text generation and judging experiment.
    text_gen_results_df = run_text_generation_experiment(
        models_to_test=settings.MODELS_TO_TEST,
        hf_handlers=hf_handlers,
        groq_generate_func=generate_response_groq,
        judge_model_id=settings.JUDGE_MODEL_ID,
        traits_definitions=prompts.TRAITS_DEFINITIONS,
        questions=prompts.QUESTIONS
    )

    # Run the BFI-44 questionnaire experiment.
    questionnaire_results_df = run_questionnaire_experiment(
        models_to_test=settings.MODELS_TO_TEST,
        hf_handlers=hf_handlers,
        groq_generate_func=generate_response_groq,
        bfi44_questions=prompts.BFI44_QUESTIONS,
        bfi44_scores_dict=prompts.BFI44_SCORES_DICT,
        traits_definitions=prompts.TRAITS_DEFINITIONS
    )

    # 4. --- SAVE RAW RESULTS ---
    # Save the DataFrames from the experiments to CSV files.
    logging.info("--- Saving Raw Experiment Results ---")
    save_dataframe_to_csv(text_gen_results_df, settings.RESULTS_DIR, settings.TEXT_GEN_RESULTS_FILENAME)
    save_dataframe_to_csv(questionnaire_results_df, settings.RESULTS_DIR, settings.QUESTIONNAIRE_RESULTS_FILENAME)

    # 5. --- PERFORM AND SAVE ANALYSIS ---
    logging.info("--- Starting Analysis and Visualization ---")

    # Generate and save the confusion matrix plots.
    plot_confusion_matrices(text_gen_results_df, settings.RESULTS_DIR, settings.CONFUSION_MATRIX_FILENAME)

    # Generate and save the questionnaire histogram plots.
    plot_questionnaire_histograms(questionnaire_results_df, prompts.BFI44_SCORES_DICT, settings.RESULTS_DIR, settings.QUESTIONNAIRE_HISTOGRAM_FILENAME)
    
    # Calculate and save the raw linguistic similarity data.
    analyze_and_save_similarity_data(text_gen_results_df, settings.RESULTS_DIR, settings.SIMILARITY_DATA_FILENAME)

    # Generate and save the linguistic similarity heatmaps.
    plot_similarity_heatmaps(text_gen_results_df, settings.RESULTS_DIR, settings.SIMILARITY_HEATMAP_FILENAME)


    # 6. --- COMPLETION ---
    print("="*80)
    logging.info("🎉🎉🎉 PROJECT COMPLETE! All experiments and analyses have finished. 🎉🎉🎉")
    logging.info(f"All results have been saved in the '{settings.RESULTS_DIR}/' directory.")
    print("="*80)


if __name__ == "__main__":
    main()

