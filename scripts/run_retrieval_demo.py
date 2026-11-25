#!/usr/bin/env python3
"""Run a deterministic toy example of LIGHT hierarchical retrieval."""

from pathlib import Path
import sys

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from light import PromptBank, hierarchical_retrieve  # noqa: E402


def main() -> None:
    image = np.array([0.95, 0.05, 0.10, 0.80])
    prompts = PromptBank(
        coarse_labels=["cerebellum", "ventricle", "frontal lobe"],
        fine_labels=[
            "left cerebellar hemisphere",
            "fourth ventricle",
            "left frontal lobe",
        ],
        subtype_labels=["glioma", "hemangioma", "meningioma"],
        coarse_positive=np.array(
            [
                [[1.0, 0.0, 0.0, 0.8], [0.9, 0.1, 0.0, 0.7]],
                [[0.1, 1.0, 0.1, 0.2], [0.0, 0.9, 0.1, 0.3]],
                [[0.0, 0.1, 1.0, 0.1], [0.1, 0.0, 0.9, 0.0]],
            ]
        ),
        coarse_negative=np.array(
            [
                [[0.0, 1.0, 0.8, 0.0]],
                [[0.8, 0.0, 0.5, 0.0]],
                [[0.8, 0.2, 0.0, 0.7]],
            ]
        ),
        fine_positive=np.array(
            [
                [[1.0, 0.0, 0.0, 0.9]],
                [[0.0, 1.0, 0.0, 0.4]],
                [[0.0, 0.0, 1.0, 0.1]],
            ]
        ),
        subtype_positive=np.array(
            [
                [[0.2, 0.8, 0.1, 0.1]],
                [[0.9, 0.0, 0.0, 1.0]],
                [[0.3, 0.4, 0.8, 0.1]],
            ]
        ),
        fine_to_coarse={
            "left cerebellar hemisphere": "cerebellum",
            "fourth ventricle": "ventricle",
            "left frontal lobe": "frontal lobe",
        },
    )
    result = hierarchical_retrieve(image, prompts)
    print("Coarse localization:", ", ".join(result.coarse_labels))
    print("Fine localization:", result.fine_label)
    print("Subtype classification:", result.subtype_label)


if __name__ == "__main__":
    main()
