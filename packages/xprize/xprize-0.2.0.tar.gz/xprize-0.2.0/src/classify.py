import numpy as np
from sklearn.ensemble import RandomForestClassifier


def classify(
    train_gt_embs: np.ndarray,
    train_labels: np.ndarray,
    query_gt_emb: np.ndarray,
) -> int:
    clf = RandomForestClassifier(n_estimators=100)
    clf.fit(train_gt_embs, train_labels)
    return clf.predict(query_gt_emb)[0]
