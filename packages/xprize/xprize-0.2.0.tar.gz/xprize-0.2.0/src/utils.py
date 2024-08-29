import time
from pathlib import Path
from typing import Tuple

import numpy as np
from scipy.spatial import distance

timer = time.perf_counter

CLASSES = {
    "Rubber Tree": "orange",
    "Brazil Nut Tree": "green",
    "River": "blue",
    "Other Tree": "gray",
}


def load_emb(npy_path: Path) -> np.ndarray:
    return np.mean(np.squeeze(np.load(npy_path)), axis=(1, 2))


def f2s(duration: float) -> str:
    if duration < 1e-6:
        return f"{duration * 1e9:.2f} ns"
    elif duration < 1e-3:
        return f"{duration * 1e6:.2f} μs"
    elif duration < 1:
        return f"{duration * 1e3:.2f} ms"
    elif duration < 60:
        return f"{duration:.2f} s"
    elif duration < 3600:
        minutes = int(duration // 60)
        seconds = int(duration % 60)
        return f"{minutes} m {seconds} s"
    else:
        hours = int(duration // 3600)
        minutes = int((duration % 3600) // 60)
        return f"{hours} h {minutes} m"


def split_sort(x: Path) -> Tuple[int, int]:
    splits = x.stem.split("_")
    return (int(splits[1]), int(splits[2]))


def int_sort(x: Path) -> int:
    return int(x.stem)


def format_func(x: str) -> str:
    return f"**:{CLASSES[x]}[{x}]**"


def compute_distance(
    x_pred: np.ndarray, x_train: np.ndarray, metric: str, aggregation: str = "min"
) -> np.ndarray:
    """
    Compute the minimum distance between the query embeddings and all embeddings based on the specified metric.
    Parameters
    ----------
    x_pred : np.ndarray
        Embeddings of all images (shape: [N, D]).
    x_train : np.ndarray
        Query embeddings (shape: [M, D]).
    metric : str
        Distance metric to use ("euclidean", "cosine", "manhattan", "chebyshev", "mahalanobis", "correlation").
    aggregation : str
        Aggregation method to use ("min", "max", "mean", "median").
    Returns
    -------
    np.ndarray
        Minimum distances between the query embeddings and all embeddings (shape: [N,]).
    """
    if metric not in [
        "euclidean",
        "cosine",
        "manhattan",
        "chebyshev",
        "correlation",
    ]:
        raise ValueError(f"Unsupported metric: {metric}")

    if aggregation not in ["min", "max", "mean", "median"]:
        raise ValueError(f"Unsupported aggregation: {aggregation}")

    dists = distance.cdist(x_pred, x_train, metric)  # (n, m)

    # Compute the minimum distance for each query embedding
    if aggregation == "min":
        dists = np.min(dists, axis=1)
    elif aggregation == "max":
        dists = np.max(dists, axis=1)
    elif aggregation == "mean":
        dists = np.mean(dists, axis=1)
    elif aggregation == "median":
        dists = np.median(dists, axis=1)
    return dists  # (n,)


def mahalanobis_distance_2d(all_embs: np.ndarray, query_embs: np.ndarray) -> np.ndarray:
    """
    Compute Mahalanobis distance between all embeddings and the query embeddings.

    Parameters
    ----------
    all_embs : np.ndarray
        Embeddings of all images (shape: [N, D]).
    query_embs : np.ndarray
        Query embeddings (shape: [M, D]).

    Returns
    -------
    np.ndarray
        Mahalanobis distance (shape: [N])
    """
    # Compute the mean of the query embeddings
    mean_query_embs = np.mean(query_embs, axis=0)  # (D,)
    print(f"{mean_query_embs.shape=}")

    # Compute the covariance matrix of the query embeddings
    cov_matrix = np.cov(query_embs, rowvar=False)  # (D, D)
    print(f"{cov_matrix.shape=}")

    # Compute the inverse of the covariance matrix
    inv_cov_matrix = np.linalg.inv(cov_matrix)  # (D, D)
    print(f"{inv_cov_matrix.shape=}")

    # Compute the Mahalanobis distance for each embedding
    diff = all_embs - mean_query_embs  # (N, D)
    mahalanobis_distances = np.sqrt(
        np.einsum("ij,ij->i", np.dot(diff, inv_cov_matrix), diff)
    )  # (N,)
    print(f"{mahalanobis_distances.shape=}")

    return mahalanobis_distances


def correlation_distance_2d(all_embs: np.ndarray, query_embs: np.ndarray) -> np.ndarray:
    """
    Compute correlation distance between all embeddings and the query embeddings.
    Parameters
    ----------
    all_embs : np.ndarray
        Embeddings of all images (shape: [N, D]).
    query_embs : np.ndarray
        Query embeddings (shape: [M, D]).
    Returns
    -------
    np.ndarray
        Correlation distances (shape: [M, N]).
    """
    all_ems_std = np.std(all_embs, axis=0)
    all_ems_std[all_ems_std == 0] = 1
    all_embs = (all_embs - np.mean(all_embs, axis=0)) / all_ems_std
    query_embs = (query_embs - np.mean(query_embs, axis=0)) / np.std(query_embs, axis=0)
    dists = np.corrcoef(all_embs, query_embs.T)[-1, :-1]
    return dists


def compute_distance_matrix(
    all_embs: np.ndarray, query_emb: np.ndarray, metric: str
) -> np.ndarray:
    """
    Compute the distance between the query embedding and all embeddings based on the specified metric.
    Parameters
    ----------
    all_embs : np.ndarray
        Embeddings of all images (shape: [N, D]).
    query_emb : np.ndarray
        Query embedding (shape: [D,]).
    metric : str
        Distance metric to use ("euclidean", "cosine", "manhattan", "chebyshev", "mahalanobis", "correlation").
    Returns
    -------
    np.ndarray
        Distances between the query embedding and all embeddings (shape: [N,]).
    """
    n, d = all_embs.shape
    assert query_emb.shape == (d,), f"query_emb.shape != {d}"

    assert not np.isnan(all_embs).any(), "all_embs contains NaNs"
    assert not np.isnan(query_emb).any(), "query_emb contains NaNs"

    if metric == "euclidean":
        dists = np.linalg.norm(all_embs - query_emb, axis=1)
    elif metric == "cosine":
        dists = np.dot(all_embs, query_emb) / (
            np.linalg.norm(all_embs, axis=1) * np.linalg.norm(query_emb)
        )
        dists = 1 - dists
        # print(f"{dists.max()=}, {dists.min()=}")
    elif metric == "manhattan":
        dists = np.sum(np.abs(all_embs - query_emb), axis=1)
    elif metric == "chebyshev":
        dists = np.max(np.abs(all_embs - query_emb), axis=1)
    elif metric == "mahalanobis":
        dists = mahalanobis_distance(all_embs, query_emb)
    elif metric == "correlation":
        dists = correlation_distance(all_embs, query_emb)
        # dists = 1 - dists
    else:
        raise ValueError(f"Unknown metric: {metric}")

    return dists


def mahalanobis_distance(all_embs: np.ndarray, query_emb: np.ndarray) -> np.ndarray:
    """
    Compute Mahalanobis distance between all embeddings and the query embedding.
    Parameters
    ----------
    all_embs : np.ndarray
        Embeddings of all images (shape: [N, D]).
    query_emb : np.ndarray
        Query embedding (shape: [D,]).
    Returns
    -------
    np.ndarray
        Mahalanobis distances (shape: [N,]).
    """
    n, d = all_embs.shape
    all_ems_std = np.std(all_embs, axis=0)
    all_ems_std[all_ems_std == 0] = 1
    all_embs = (all_embs - np.mean(all_embs, axis=0)) / all_ems_std
    cov = np.cov(all_embs, rowvar=False) + np.eye(d) * 1e-8
    inv_cov = np.linalg.inv(cov)
    delta = all_embs - query_emb
    return np.sqrt(delta @ inv_cov @ delta.T).diagonal()


def correlation_distance(all_embs: np.ndarray, query_emb: np.ndarray) -> np.ndarray:
    """
    Compute correlation distance between all embeddings and the query embedding.
    Parameters
    ----------
    all_embs : np.ndarray
        Embeddings of all images (shape: [N, D]).
    query_emb : np.ndarray
        Query embedding (shape: [D,]).
    Returns
    -------
    np.ndarray
        Correlation distances (shape: [N,]).
    """
    all_ems_std = np.std(all_embs, axis=0)
    all_ems_std[all_ems_std == 0] = 1
    all_embs = (all_embs - np.mean(all_embs, axis=0)) / all_ems_std
    query_emb = (query_emb - np.mean(query_emb)) / np.std(query_emb)
    dists = np.corrcoef(all_embs, query_emb)[-1, :-1]
    return dists
