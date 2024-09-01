from .metrics import (
    mean_pairwise_distance, 
    variance_pairwise_distance,
    mean_cosine_similarity,
    variance_cosine_similarity,
    entropy_value
)

def evaluate_embeddings(embeddings):
    return {
        "mean_pairwise_distance": mean_pairwise_distance(embeddings),
        "variance_pairwise_distance": variance_pairwise_distance(embeddings),
        "mean_cosine_similarity": mean_cosine_similarity(embeddings),
        "variance_cosine_similarity": variance_cosine_similarity(embeddings),
        "entropy_value": entropy_value(embeddings)
    }
