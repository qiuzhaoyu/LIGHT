# Source Code

This directory contains a lightweight public reference implementation of the
algorithmic parts of LIGHT that do not depend on private clinical data or
unreleased model weights.

## Implemented Reference Modules

```text
src/
+-- light/
    +-- __init__.py
    +-- losses.py        # Symmetric InfoNCE and downstream multi-task losses
    +-- retrieval.py     # Multi-template scoring and hierarchical retrieval
```

The reference code follows the three stages described in the manuscript:

1. **Large-scale foundation pretraining** aligns multimodal 3D MRI and
   structured report embeddings with symmetric InfoNCE loss.
2. **Grounded task fine-tuning** optimizes coarse localization, fine
   localization, and subtype retrieval losses from a shared tumor-centered
   image embedding.
3. **Hierarchical joint retrieval** thresholds differential coarse-region
   scores, restricts fine-grained candidates to the predicted coarse regions,
   and retrieves the subtype from positive prompt similarities.

For multi-template prompts, each prompt is scored separately. Class-level
scores are averages of template-specific similarities, rather than cosine
similarities computed from averaged raw text embeddings.

## Public Release Boundary

The current implementation intentionally accepts pre-computed embeddings. It
does not include private data loaders, clinical preprocessing paths, trained
weights, or an unreleased encoder implementation. These components can be
connected later without changing the retrieval interface.

Install the minimal dependency set from the repository root before running the
reference utilities:

```bash
pip install -r requirements.txt
```
