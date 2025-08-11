# utils/helpers.py

import pandas as pd
import os
import logging

def ensure_dir_exists(directory_path: str):
    """
    Checks if a directory exists, and if not, creates it.

    Args:
        directory_path (str): The path to the directory.
    """
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
        logging.info(f"Created directory: {directory_path}")

def save_dataframe_to_csv(df: pd.DataFrame, directory: str, filename: str):
    """
    Saves a pandas DataFrame to a CSV file in the specified directory.

    Args:
        df (pd.DataFrame): The DataFrame to save.
        directory (str): The directory where the file will be saved.
        filename (str): The name of the CSV file.
    """
    if df.empty:
        logging.warning(f"DataFrame is empty. Skipping save for '{filename}'.")
        return

    ensure_dir_exists(directory)
    output_path = os.path.join(directory, filename)
    
    try:
        df.to_csv(output_path, index=False)
        logging.info(f"✅ Successfully saved results to '{output_path}'")
    except Exception as e:
        logging.error(f"Failed to save DataFrame to '{output_path}'. Error: {e}")

