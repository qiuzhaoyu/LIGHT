# LIGHT

**Learning Image-Text Grounding for Hierarchical Brain Tumor Localization and Subtype Classification in Multimodal MRI**

This repository will host the code, documentation, sample data, and reproducible assets for LIGHT. The project is under active preparation; the current version provides a lightweight public scaffold with manuscript figures and release placeholders.

## Overview

LIGHT formulates brain tumor localization and subtype classification as a unified image-text retrieval problem. Given multimodal brain MRI, the model retrieves human-readable anatomical and subtype prompts for hierarchical tumor localization and subtype prediction.

## Framework

![LIGHT framework](assets/figures/framework.png)

LIGHT combines multimodal MRI encoding with text-side anatomical and subtype prompts. The model is trained to align image features with human-readable prompt embeddings, so localization and subtype classification can be expressed as retrieval over explicit clinical concepts.

## Repository Layout

```text
LIGHT/
+-- assets/
|   +-- figures/          # README figures and source PDFs
|       +-- source/       # Source PDFs copied from the manuscript
+-- checkpoints/          # Model checkpoints or download instructions
+-- data/                 # Data access notes and sample metadata
+-- docs/                 # Extra documentation
+-- examples/             # Minimal usage examples
+-- scripts/              # Utility scripts
+-- src/                  # Core implementation
```

## Results

### Dataset And Validation Summary

![Dataset and validation summary](assets/figures/data_summary.png)

The study includes in-house, external clinical, and public validation cohorts. This figure summarizes the cohort composition and the role of each dataset in localization, subtype classification, and public validation experiments.

### LLM-Assisted Label Validation

![LLM-assisted label validation](assets/figures/llm_validation.png)

Structured report information is used to support label construction. The validation figure summarizes the manual review process and the agreement of LLM-assisted extraction with expert-verified labels.

### Ablation Summary

![Ablation summary](assets/figures/ablation.png)

The ablation study evaluates the contribution of foundation pretraining, prompt design, model components, and modality settings. Numerical result tables will be added after the final manuscript values are locked.

### Qualitative Examples

![Qualitative retrieval examples](assets/figures/qualitative_tsne.png)

The embedding visualization provides a qualitative view of how image-text grounding separates anatomical or subtype concepts in the learned representation space.

![Grad-CAM visualization](assets/figures/qualitative_gradcam.png)

The attention visualization illustrates the regions that contribute to the retrieved localization and subtype hypotheses.

## Figure Sources

The README images are rendered as white-background PNG files for readability in both light and dark GitHub themes. Original manuscript PDFs are kept in [`assets/figures/source`](assets/figures/source) for later replacement or higher-resolution export.

## Installation

The full environment file will be released with the implementation. A provisional setup flow is:

```bash
git clone https://github.com/qiuzhaoyu/LIGHT.git
cd LIGHT
conda create -n light python=3.10
conda activate light
pip install -r requirements.txt
```

## Data

Clinical data cannot be redistributed directly. Public data links, sample metadata, and preprocessing notes will be documented in [`data/data.md`](data/data.md).

## Code Release Plan

- [ ] Preprocessing scripts
- [ ] Prompt vocabulary construction
- [ ] Model definition
- [ ] Training and evaluation scripts
- [ ] Checkpoint/download instructions
- [ ] Sample data and inference demo

## Citation

Citation information will be added after publication.

## Contact

For questions, please open an issue or contact the repository maintainer.
