# Covertype ML Comparison

Multiclass model comparison for the Forest Cover Type dataset. The notebook follows the analysis workflow from the earlier Zomato project and adds expanded EDA, stratified cross validation, per class evaluation, multiclass ROC curves, and feature importance.

## Contents

- `Covertype_ML_Comparison.ipynb` — analysis notebook
- `covertype.zip` — dataset archive used by the notebook
- `requirements.txt` — Python dependencies

## Run

Install the dependencies, open the notebook in Jupyter, and run the cells from top to bottom:

```bash
python -m pip install -r requirements.txt
jupyter lab Covertype_ML_Comparison.ipynb
```

Keep `covertype.zip` beside the notebook. In Google Colab, the data loading cell prompts you to upload the ZIP if it is not already in the runtime.

The notebook reads the compressed data directly from the ZIP, so you do not need to extract it first. To use an archive in another location, set the `DATA_ZIP` variable in the notebook.

The dataset contains 581,012 observations, 54 predictor columns, and seven forest cover classes. The three compared classifiers are multinomial logistic regression, random forest, and histogram gradient boosting.
