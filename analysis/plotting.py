# analysis/plotting.py

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import logging

def plot_confusion_matrices(results_df: pd.DataFrame, output_dir: str, filename: str):
    """
    Generates and saves confusion matrix plots for the main experiment results.

    Args:
        results_df (pd.DataFrame): The DataFrame from the text generation experiment.
        output_dir (str): The directory to save the plot image.
        filename (str): The filename for the saved plot image.
    """
    logging.info("Generating confusion matrix plots...")

    def map_prompted_score(value):
        if value in [1, 2]: return 'low'
        elif value == 3: return 'medium'
        elif value in [4, 5]: return 'high'
        return None

    def map_detected_score(value):
        try:
            value = int(float(value))
            if value in [-2, -1]: return 'low'
            elif value == 0: return 'medium'
            elif value in [1, 2]: return 'high'
        except (ValueError, TypeError):
            return None
        return None

    df_plot = results_df.copy()
    df_plot = df_plot.dropna(subset=['prompted_score', 'judge_score', 'judge_decision_type'])
    df_plot = df_plot[df_plot['judge_decision_type'] != 'Nondistinguishable']
    
    if df_plot.empty:
        logging.warning("No data available to plot for the main experiment after filtering.")
        return

    df_plot['Prompted Category'] = df_plot['prompted_score'].apply(map_prompted_score)
    df_plot['Detected Category'] = df_plot['judge_score'].apply(map_detected_score)
    
    model_keys = df_plot['model_key'].unique()
    traits = df_plot['prompted_trait'].unique()
    n_rows, n_cols = len(model_keys), len(traits)
    score_categories = ['low', 'medium', 'high']

    if n_rows == 0 or n_cols == 0:
        logging.warning("Not enough dimensions to create confusion matrix plot.")
        return

    fig, axes = plt.subplots(n_rows, n_cols, figsize=(5 * n_cols, 5 * n_rows), squeeze=False)
    for m, model_key in enumerate(model_keys):
        for t, trait_name in enumerate(traits):
            ax = axes[m, t]
            df_subset = df_plot[(df_plot['model_key'] == model_key) & (df_plot['prompted_trait'] == trait_name)]
            
            if df_subset.empty:
                ax.text(0.5, 0.5, 'No Data', ha='center', va='center')
                ax.set_xticks([])
                ax.set_yticks([])
            else:
                cm = pd.crosstab(df_subset['Prompted Category'], df_subset['Detected Category'], rownames=['Prompted'], colnames=['Detected'], dropna=False)
                cm = cm.reindex(index=score_categories, columns=score_categories, fill_value=0)
                sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=ax, cbar=False)
            
            ax.set_title(trait_name)
            if t == 0: ax.set_ylabel(f"{model_key}\n\nPrompted", fontsize=12)
            else: ax.set_ylabel('')
            if m == n_rows - 1: ax.set_xlabel("Detected", fontsize=12)
            else: ax.set_xlabel('')

    plt.tight_layout(pad=3.0)
    plt.suptitle("Confusion Matrices of Prompted vs. Detected Personality Traits", fontsize=16, y=1.02)
    
    output_path = os.path.join(output_dir, filename)
    plt.savefig(output_path, bbox_inches='tight', dpi=300)
    plt.show()
    logging.info(f"✅ Successfully saved confusion matrices to '{output_path}'")


def plot_questionnaire_histograms(questionnaire_df: pd.DataFrame, scores_dict: dict, output_dir: str, filename: str):
    """
    Generates and saves histogram plots for the questionnaire experiment results.

    Args:
        questionnaire_df (pd.DataFrame): The DataFrame from the questionnaire experiment.
        scores_dict (dict): The dictionary mapping text answers to scores.
        output_dir (str): The directory to save the plot image.
        filename (str): The filename for the saved plot image.
    """
    logging.info("Generating questionnaire histogram plots...")

    if questionnaire_df.empty:
        logging.warning("No data available to plot for the questionnaire experiment.")
        return

    def adjusted_score(row):
        if row['Q_type'] == 'inverted':
            return 6 - row['Scores']
        return row['Scores']

    def match_score(answer, scores_mapping):
        answer_clean = str(answer).strip().lower()
        for text, score in scores_mapping.items():
            if text in answer_clean:
                return score
        return 3 # Default to neutral if no match

    df_plot = questionnaire_df.copy()
    df_plot['Scores'] = df_plot['Answer'].apply(lambda x: match_score(x, scores_dict))
    df_plot['Adjusted Scores'] = df_plot.apply(adjusted_score, axis=1)

    model_keys = df_plot['model_key'].unique()
    traits = df_plot['trait'].unique()
    n_rows, n_cols = len(model_keys), len(traits)
    colors = {'high': '#e26952', 'low': '#6788ee'}

    if n_rows == 0 or n_cols == 0:
        logging.warning("Not enough dimensions to create questionnaire histogram plot.")
        return

    fig, axes = plt.subplots(n_rows, n_cols, figsize=(5 * n_cols, 5 * n_rows), squeeze=False)
    for m, model_key in enumerate(model_keys):
        for t, trait_name in enumerate(traits):
            ax = axes[m, t]
            data = df_plot[(df_plot['model_key'] == model_key) & (df_plot['trait'] == trait_name)]
            
            if data.empty:
                ax.axis('off')
                continue
            
            sns.histplot(data=data, x='Adjusted Scores', hue='prompted_level', palette=colors, stat='probability', element="step", kde=True, ax=ax, alpha=0.7, linewidth=3)
            ax.set_title(trait_name)
            ax.set_xlim((1, 5))
            
            if t == 0: ax.set_ylabel(model_key, fontsize=14)
            else: ax.set_ylabel('')
            if m == n_rows - 1: ax.set_xlabel("Average Score", fontsize=12)
            else: ax.set_xlabel('')
            
            handles, labels = ax.get_legend_handles_labels()
            ax.legend(handles, labels, title=None, frameon=False, loc='upper center', bbox_to_anchor=(0.5, 1.15), ncol=2)

    plt.tight_layout(pad=3.0)
    plt.suptitle("Distribution of BFI-44 Scores for Prompted Personas", fontsize=16, y=1.03)

    output_path = os.path.join(output_dir, filename)
    plt.savefig(output_path, bbox_inches='tight', dpi=300)
    plt.show()
    logging.info(f"✅ Successfully saved questionnaire histograms to '{output_path}'")
