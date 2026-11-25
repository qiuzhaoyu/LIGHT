"""Reference implementation of LIGHT hierarchical joint retrieval.

The released helper operates on pre-computed image and prompt embeddings. It
keeps the retrieval behavior inspectable without assuming a private encoder,
checkpoint, or clinical data loader.
"""

from dataclasses import dataclass
from typing import Mapping, Sequence

import numpy as np


Array = np.ndarray


def _normalize(values: Array) -> Array:
    values = np.asarray(values, dtype=np.float64)
    norms = np.linalg.norm(values, axis=-1, keepdims=True)
    return values / np.maximum(norms, 1e-12)


def _template_scores(image_embedding: Array, prompt_embeddings: Array) -> Array:
    """Average template-specific cosine similarities for each class."""
    image_embedding = _normalize(np.asarray(image_embedding).reshape(1, -1))[0]
    prompt_embeddings = _normalize(prompt_embeddings)
    if prompt_embeddings.ndim != 3:
        raise ValueError("prompt embeddings must have shape [classes, templates, dim]")
    if prompt_embeddings.shape[-1] != image_embedding.shape[-1]:
        raise ValueError("image and prompt embeddings must share the same dimension")
    return np.mean(prompt_embeddings @ image_embedding, axis=1)


def _sigmoid(values: Array) -> Array:
    return 1.0 / (1.0 + np.exp(-np.clip(values, -60.0, 60.0)))


@dataclass(frozen=True)
class PromptBank:
    """Pre-computed text-side prompt embeddings and vocabulary metadata."""

    coarse_labels: Sequence[str]
    fine_labels: Sequence[str]
    subtype_labels: Sequence[str]
    coarse_positive: Array
    coarse_negative: Array
    fine_positive: Array
    subtype_positive: Array
    fine_to_coarse: Mapping[str, str]


@dataclass(frozen=True)
class RetrievalResult:
    """Human-readable LIGHT predictions and class-level retrieval scores."""

    coarse_labels: list[str]
    fine_label: str
    subtype_label: str
    coarse_scores: dict[str, float]
    fine_scores: dict[str, float]
    subtype_scores: dict[str, float]


def _validate_bank(bank: PromptBank) -> None:
    expected = (
        ("coarse_positive", bank.coarse_positive, len(bank.coarse_labels)),
        ("coarse_negative", bank.coarse_negative, len(bank.coarse_labels)),
        ("fine_positive", bank.fine_positive, len(bank.fine_labels)),
        ("subtype_positive", bank.subtype_positive, len(bank.subtype_labels)),
    )
    for name, values, classes in expected:
        if np.asarray(values).ndim != 3 or np.asarray(values).shape[0] != classes:
            raise ValueError(f"{name} must have shape [{classes}, templates, dim]")
    unknown = set(bank.fine_labels) - set(bank.fine_to_coarse)
    if unknown:
        raise ValueError(f"fine_to_coarse is missing labels: {sorted(unknown)}")


def hierarchical_retrieve(
    image_embedding: Array,
    prompts: PromptBank,
    coarse_threshold: float = 0.5,
) -> RetrievalResult:
    """Retrieve coarse regions, one constrained fine region, and one subtype.

    Coarse localization uses differential positive-minus-negative similarity
    followed by thresholding. Fine localization is restricted to subregions
    under the predicted coarse set. Subtype retrieval uses positive scores.
    """
    _validate_bank(prompts)
    coarse_positive = _template_scores(image_embedding, prompts.coarse_positive)
    coarse_negative = _template_scores(image_embedding, prompts.coarse_negative)
    coarse_differential = coarse_positive - coarse_negative
    coarse_probabilities = _sigmoid(coarse_differential)

    selected_indices = np.flatnonzero(coarse_probabilities >= coarse_threshold)
    if selected_indices.size == 0:
        selected_indices = np.asarray([int(np.argmax(coarse_differential))])
    selected_coarse = [prompts.coarse_labels[index] for index in selected_indices]

    fine_scores = _template_scores(image_embedding, prompts.fine_positive)
    candidate_indices = [
        index
        for index, label in enumerate(prompts.fine_labels)
        if prompts.fine_to_coarse[label] in selected_coarse
    ]
    if not candidate_indices:
        raise ValueError("predicted coarse labels do not contain any fine candidates")
    fine_index = max(candidate_indices, key=lambda index: fine_scores[index])

    subtype_scores = _template_scores(image_embedding, prompts.subtype_positive)
    subtype_index = int(np.argmax(subtype_scores))

    return RetrievalResult(
        coarse_labels=selected_coarse,
        fine_label=prompts.fine_labels[fine_index],
        subtype_label=prompts.subtype_labels[subtype_index],
        coarse_scores=dict(zip(prompts.coarse_labels, coarse_differential.tolist())),
        fine_scores=dict(zip(prompts.fine_labels, fine_scores.tolist())),
        subtype_scores=dict(zip(prompts.subtype_labels, subtype_scores.tolist())),
    )
