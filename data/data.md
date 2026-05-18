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
