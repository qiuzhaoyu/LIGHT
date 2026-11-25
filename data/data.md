# Data

This folder documents data availability and sample-data preparation for LIGHT.

## Clinical Data

The private clinical MRI datasets used in the study cannot be redistributed directly. Future releases can include:

- Cohort summary tables
- Preprocessing and quality-control notes
- De-identified sample metadata
- Instructions for reproducing public-dataset experiments

## Public Data

Public datasets and download instructions will be listed here after final verification.

## Coarse-Region Vocabulary

The public coarse-region vocabulary overview is available in
[`location_vocabulary/`](location_vocabulary/):

- [`coarse_regions_21.csv`](location_vocabulary/coarse_regions_21.csv): 21
  coarse anatomical regions.

This file contains anatomical vocabulary entries only. It does not include
case IDs, report text, diagnoses, disease categories, image paths, dates, or MRI
sequence names.

## Expected Sample Layout

```text
data/
+-- samples/
|   +-- images/
|   +-- masks/
|   +-- metadata.csv
+-- data.md
```

Do not commit private raw imaging data or identifiable metadata.
