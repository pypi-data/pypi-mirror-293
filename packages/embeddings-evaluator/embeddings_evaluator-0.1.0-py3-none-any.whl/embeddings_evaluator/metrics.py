import numpy as np
from sklearn.metrics import pairwise_distances
from scipy.stats import entropy
from sklearn.decomposition import PCA

def mean_pairwise_distance(embeddings):
    distances = pairwise_distances(embeddings)
    return np.mean(distances)

def variance_pairwise_distance(embeddings):
    distances = pairwise_distances(embeddings)
    return np.var(distances)

def mean_cosine_similarity(embeddings):
    similarities = 1 - pairwise_distances(embeddings, metric='cosine')
    return np.mean(similarities)

def variance_cosine_similarity(embeddings):
    similarities = 1 - pairwise_distances(embeddings, metric='cosine')
    return np.var(similarities)

def entropy_value(embeddings):
    pca = PCA(n_components=0.95)
    reduced = pca.fit_transform(embeddings)
    hist, _ = np.histogram(reduced, bins=100)
    return entropy(hist)
