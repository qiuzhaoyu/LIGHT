"""NumPy reference losses corresponding to the LIGHT manuscript."""

from typing import Iterable

import numpy as np


Array = np.ndarray


def _log_softmax(values: Array, axis: int = -1) -> Array:
    values = np.asarray(values, dtype=np.float64)
    maximum = np.max(values, axis=axis, keepdims=True)
    shifted = values - maximum
    return shifted - np.log(np.sum(np.exp(shifted), axis=axis, keepdims=True))


def clip_loss(image_embeddings: Array, text_embeddings: Array, temperature: float) -> float:
    """Symmetric InfoNCE loss for foundation pretraining."""
    if temperature <= 0:
        raise ValueError("temperature must be positive")
    image_embeddings = np.array(image_embeddings, dtype=np.float64, copy=True)
    text_embeddings = np.array(text_embeddings, dtype=np.float64, copy=True)
    image_embeddings /= np.maximum(np.linalg.norm(image_embeddings, axis=1, keepdims=True), 1e-12)
    text_embeddings /= np.maximum(np.linalg.norm(text_embeddings, axis=1, keepdims=True), 1e-12)
    logits = image_embeddings @ text_embeddings.T / temperature
    labels = np.arange(logits.shape[0])
    image_to_text = -_log_softmax(logits, axis=1)[labels, labels]
    text_to_image = -_log_softmax(logits.T, axis=1)[labels, labels]
    return float(np.mean((image_to_text + text_to_image) / 2.0))


def _binary_cross_entropy(logits: Array, targets: Array) -> float:
    logits = np.asarray(logits, dtype=np.float64)
    targets = np.asarray(targets, dtype=np.float64)
    return float(np.mean(np.maximum(logits, 0.0) - logits * targets + np.log1p(np.exp(-np.abs(logits)))))


def _cross_entropy(logits: Array, targets: Iterable[int]) -> float:
    logits = np.asarray(logits, dtype=np.float64)
    targets = np.asarray(list(targets), dtype=np.int64)
    return float(np.mean(-_log_softmax(logits, axis=1)[np.arange(logits.shape[0]), targets]))


def downstream_loss(
    coarse_logits: Array,
    coarse_targets: Array,
    fine_logits: Array,
    fine_targets: Iterable[int],
    subtype_logits: Array,
    subtype_targets: Iterable[int],
    weights: tuple[float, float, float] = (1.0, 1.0, 1.0),
) -> dict[str, float]:
    """Weighted coarse BCE plus fine and subtype cross-entropy losses."""
    coarse = _binary_cross_entropy(coarse_logits, coarse_targets)
    fine = _cross_entropy(fine_logits, fine_targets)
    subtype = _cross_entropy(subtype_logits, subtype_targets)
    total = weights[0] * coarse + weights[1] * fine + weights[2] * subtype
    return {"total": total, "coarse": coarse, "fine": fine, "subtype": subtype}
