import pandas as pd
import matplotlib.pyplot as plt
from .evaluation import evaluate_embeddings

def compare_embeddings(embeddings_list, labels):
    """
    Compare a list of embeddings and return a DataFrame with the evaluation metrics.

    Parameters:
    embeddings_list (list of np.ndarray): List of embeddings to compare.
    labels (list of str): List of labels corresponding to each embedding.

    Returns:
    pd.DataFrame: A DataFrame containing the metrics for each embedding.
    """
    results = []

    for embeddings, label in zip(embeddings_list, labels):
        metrics = evaluate_embeddings(embeddings)
        metrics['label'] = label
        results.append(metrics)

    df = pd.DataFrame(results)
    return df

def plot_metrics(df):
    """
    Plot all metrics from the DataFrame.

    Parameters:
    df (pd.DataFrame): DataFrame containing the metrics for each embedding.
    """
    df.set_index('label').plot(kind='bar', subplots=True, layout=(3, 2), figsize=(14, 12), legend=False)
    plt.suptitle("Comparison of Embedding Metrics")
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.show()

