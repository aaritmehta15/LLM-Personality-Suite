# LLM Personality Simulation & Analysis Suite

This repository contains a comprehensive analytical framework for evaluating the ability of Large Language Models (LLMs) to simulate human personality traits based on the Big Five model (Openness, Conscientiousness, Extraversion, Agreeableness, Neuroticism).

Inspired by the methodology outlined in the paper ["Exploring the Potential of Large Language Models to Simulate Personality"](https://arxiv.org/html/2502.08265v1#:~:text=personality%20and%20conducting%20prompt%20engineering,framework%20developed%20for%20this%20study) by Molchanova et al. (2025), this project provides a robust, modular, and extensible toolkit to probe, generate, and analyze personality-aligned text from various LLMs. It serves as a practical implementation for researchers and developers interested in the nuanced aspects of model alignment, personalization, and controllable generation.

## Key Features

### Dual-Experiment Design
Employs two distinct methods to test personality simulation:
- **Questionnaire Analysis**: Models answer the BFI-44 personality questionnaire to test their understanding of trait-associated behaviors.
- **Generative Analysis**: Models generate free-form text in response to open-ended questions while being prompted with specific personality scores.

### Multi-Model Evaluation
The framework is designed to test and compare multiple models simultaneously (e.g., local Hugging Face models and API-based models like Groq).

### Automated Judging
Utilizes a powerful "judge" LLM to classify the generated texts, providing a scalable method for evaluating the simulated personalities.

### In-Depth Analysis
Automatically generates three key types of analysis from the experimental results:
- **Confusion Matrices**: To visualize the accuracy of prompted vs. detected personality levels (low, medium, high).
- **Score Distribution Histograms**: To analyze model responses to the BFI-44 questionnaire.
- **Linguistic Similarity Heatmaps**: To measure the lexical consistency of texts generated with different personality scores.

### Modular & Extensible
The codebase is highly modular, making it easy to add new models, change prompts, or introduce new analysis methods.

## Architecture

This project is organized into a modular structure to ensure clarity, maintainability, and ease of extension. The core logic is intentionally separated from the data, model handlers, and analysis scripts.

```
personality_assessment_suite/
├── 📂 analysis/         # Scripts for data processing and visualization.
├── 📂 config/           # All configuration, prompts, and static data.
├── 📂 core/             # The sacred, unaltered core experiment logic.
├── 📂 models/           # Handlers for interacting with LLMs.
├── 📂 results/          # Default output directory for all CSVs and plots.
├── 📂 utils/            # Helper functions and common utilities.
├── main.py              # The main entry point to run the entire suite.
└── requirements.txt     # Project dependencies for installation.
```

### Directory Breakdown

- **`/config`**: Contains all static data. `settings.py` manages API keys, model IDs, and filenames. `prompts.py` stores all the text for prompts, questions, and trait definitions.
- **`/core`**: The heart of the project. `experiments.py` houses the unaltered, sacred loops for the text generation and questionnaire experiments.
- **`/models`**: Manages all interactions with the LLMs. `handlers.py` contains the classes and functions for communicating with Hugging Face and Groq models.
- **`/analysis`**: Holds all scripts for processing the raw data. This includes `plotting.py` for generating graphs and `similarity.py` for the linguistic analysis.
- **`/utils`**: Contains helper functions, such as `helpers.py` for saving dataframes to CSV files.
- **`/results`**: The designated output folder where all generated CSV files and plots are saved.
- **`main.py`**: The central orchestrator. Running this script executes the entire workflow from model initialization to final analysis.

## Installation and Usage

Follow these steps to set up and run the personality analysis suite on your local machine.

### 1. Prerequisites

- Python 3.8 or newer.
- Git command-line tools.

### 2. Installation

First, clone the repository to your local machine and navigate into the project directory.

```bash
# Clone the repository
git clone https://github.com/your-username/personality_assessment_suite.git

# Navigate into the project folder
cd personality_assessment_suite
```

Next, install all the required Python packages using the requirements.txt file. It is highly recommended to do this within a virtual environment.

```bash
# Create a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

# Install dependencies
pip install -r requirements.txt
```

### 3. Configuration

This project requires API keys for Groq and Hugging Face. The script is configured to load these from Google Colab secrets by default. To run locally, you will need to modify `config/settings.py` to load these keys from environment variables or another secure source.

For example, you could change:
```python
GROQ_API_KEY = userdata.get('GROQ_API_KEY')
```
to
```python
GROQ_API_KEY = os.environ.get('GROQ_API_KEY')
```

You would then need to set the `GROQ_API_KEY` and `HF_TOKEN` environment variables in your system.

### 4. Running the Experiment

Once the installation and configuration are complete, you can run the entire experimental suite with a single command from the root directory of the project:

```bash
python main.py
```

The script will provide real-time logging updates in your terminal, showing the progress of the experiments and analysis.

### 5. Viewing the Results

All output files, including the raw data CSVs and the analysis plots (PNG images), will be automatically saved in the `/results` directory.