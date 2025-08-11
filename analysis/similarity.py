# analysis/similarity.py

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os
import logging

def _calculate_similarity_matrix(df: pd.DataFrame) -> np.ndarray:
    """
    Internal helper function to calculate a 5x5 cosine similarity matrix.
    
    It vectorizes text using TF-IDF and computes the similarity between the
    average vectors for each prompted score (1 through 5).

    Args:
        df (pd.DataFrame): A DataFrame containing 'generated_text' and 'prompted_score'.

    Returns:
        np.ndarray: A 5x5 numpy array representing the similarity matrix.
    """
    df = df.reset_index(drop=True)
    vectorizer = TfidfVectorizer(stop_words='english', min_df=2)
    
    try:
        tfidf_matrix = vectorizer.fit_transform(df['generated_text'])
    except ValueError:
        # This can happen if all documents are empty or have only stop words.
        logging.warning("TF-IDF Vectorizer failed, likely due to insufficient vocabulary. Returning an empty matrix.")
        return np.zeros((5, 5))

    score_vectors = []
    for score in range(1, 6):
        indices = df.index[df['prompted_score'] == score].tolist()
        if indices:
            mean_vector = tfidf_matrix[indices].mean(axis=0)
            score_vectors.append(mean_vector)
        else:
            # If no texts for a score, append a zero vector to maintain the 5x5 shape
            score_vectors.append(np.zeros((1, tfidf_matrix.shape[1])))

    score_vectors_matrix = np.asarray(np.vstack(score_vectors))
    similarity_matrix = cosine_similarity(score_vectors_matrix)
    return similarity_matrix

def analyze_and_save_similarity_data(results_df: pd.DataFrame, output_dir: str, filename: str):
    """
    Calculates linguistic similarity for all models and traits and saves the raw data to a CSV.

    Args:
        results_df (pd.DataFrame): The main experiment results.
        output_dir (str): The directory to save the output CSV.
        filename (str): The filename for the output CSV.
    """
    logging.info("Calculating and saving linguistic similarity data...")
    text_data = results_df[['model_key', 'prompted_trait', 'prompted_score', 'generated_text']].copy()
    text_data.dropna(subset=['generated_text'], inplace=True)

    similarity_data_list = []
    model_keys = text_data['model_key'].unique()
    traits = text_data['prompted_trait'].unique()

    for model_key in model_keys:
        for trait_name in traits:
            df_subset = text_data[(text_data['model_key'] == model_key) & (text_data['prompted_trait'] == trait_name)]
            if not df_subset.empty:
                matrix = _calculate_similarity_matrix(df_subset)
                for i in range(5):
                    for j in range(5):
                        similarity_data_list.append({
                            "model_key": model_key,
                            "trait": trait_name,
                            "prompted_score_1": i + 1,
                            "prompted_score_2": j + 1,
                            "similarity_score": matrix[i, j]
                        })

    similarity_df = pd.DataFrame(similarity_data_list)
    output_path = os.path.join(output_dir, filename)
    similarity_df.to_csv(output_path, index=False)
    logging.info(f"✅ Successfully saved raw similarity data to '{output_path}'")


def plot_similarity_heatmaps(results_df: pd.DataFrame, output_dir: str, filename: str):
    """
    Generates and saves linguistic similarity heatmap plots.

    Args:
        results_df (pd.DataFrame): The main experiment results.
        output_dir (str): The directory to save the plot image.
        filename (str): The filename for the saved plot image.
    """
    logging.info("Generating linguistic similarity heatmaps...")
    text_data = results_df[['model_key', 'prompted_trait', 'prompted_score', 'generated_text']].copy()
    text_data.dropna(subset=['generated_text'], inplace=True)

    model_keys = text_data['model_key'].unique()
    traits = text_data['prompted_trait'].unique()
    n_rows, n_cols = len(model_keys), len(traits)

    if n_rows == 0 or n_cols == 0:
        logging.warning("Not enough dimensions to create similarity heatmap plot.")
        return

    fig, axes = plt.subplots(n_rows, n_cols, figsize=(5 * n_cols, 5 * n_rows), squeeze=False)

    for m, model_key in enumerate(model_keys):
        for t, trait_name in enumerate(traits):
            ax = axes[m, t]
            df_subset = text_data[(text_data['model_key'] == model_key) & (text_data['prompted_trait'] == trait_name)]

            if df_subset.empty:
                ax.text(0.5, 0.5, 'No Data', ha='center', va='center')
            else:
                similarity_matrix = _calculate_similarity_matrix(df_subset)
                sns.heatmap(similarity_matrix, annot=True, fmt=".2f", cmap="coolwarm",
                            xticklabels=range(1, 6), yticklabels=range(1, 6),
                            ax=ax, vmin=0, vmax=1)
                ax.set_title(trait_name)
                ax.set_xlabel("Prompted Score")

            if t == 0:
                ax.set_ylabel(f"{model_key}\n\nPrompted Score", fontsize=12)
            else:
                ax.set_ylabel('')

    plt.suptitle("Linguistic Similarity of Generated Texts by Prompted Score", fontsize=16, y=1.02)
    plt.tight_layout(rect=[0, 0, 1, 0.98])

    output_path = os.path.join(output_dir, filename)
    plt.savefig(output_path, bbox_inches='tight', dpi=300)
    plt.show()
    logging.info(f"✅ Successfully saved similarity heatmaps to '{output_path}'")
