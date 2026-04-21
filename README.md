# ML_Project

Alternate feature extract:
- direct JSON lookup rather than 'in' keyword scanning
- one-hot for nominal vars rather than ordinal
- ordinal encodings for categoricals
- pd.NA to distinguish missing entries from ones that are 0
- ECOG score, prior malignancy, and laterality feature extraction
- dictionary use to cut down on if else

Those are some of the differences between alternate_feature_extract.py and import_clinical.py