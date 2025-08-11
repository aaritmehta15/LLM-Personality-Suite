# config/settings.py

import os
from google.colab import userdata
from huggingface_hub import login
import logging

# --- API and Authentication Configuration ---

try:
    # Attempt to load keys from Google Colab secrets
    GROQ_API_KEY = userdata.get('GROQ_API_KEY')
    HF_TOKEN = userdata.get('HF_TOKEN')

    # Set environment variable for the Groq client
    os.environ["GROQ_API_KEY"] = GROQ_API_KEY

    # Log in to Hugging Face Hub
    login(token=HF_TOKEN)

    logging.info("✅ Groq and Hugging Face keys loaded and configured successfully.")

except Exception as e:
    logging.warning(f"⚠️ Could not load keys from Colab secrets. Please ensure they are set correctly. Error: {e}")
    GROQ_API_KEY = None
    HF_TOKEN = None

# --- Model Definitions ---

# Defines the models to be used in the experiments and their handlers.
# 'handler' can be 'hf' (Hugging Face) or 'groq'.
MODELS_TO_TEST = {
    "Gemma-7B (Hugging Face)": {"handler": "hf", "model_id": "google/gemma-7b-it"},
    "Llama-3.1-8B (Groq)": {"handler": "groq", "model_id": "llama-3.1-8b-instant"}
}

# The model used for judging the generated text.
JUDGE_MODEL_ID = "llama3-70b-8192"


# --- Output File Configuration ---

# A dedicated directory to store all output files.
RESULTS_DIR = "results"

# Filenames for the output CSV files.
TEXT_GEN_RESULTS_FILENAME = "text_generation_results.csv"
QUESTIONNAIRE_RESULTS_FILENAME = "questionnaire_results.csv"
SIMILARITY_DATA_FILENAME = "linguistic_similarity_data.csv"

# Filenames for the output plot images.
CONFUSION_MATRIX_FILENAME = "confusion_matrices.png"
QUESTIONNAIRE_HISTOGRAM_FILENAME = "questionnaire_histograms.png"
SIMILARITY_HEATMAP_FILENAME = "linguistic_similarity_heatmap.png"
