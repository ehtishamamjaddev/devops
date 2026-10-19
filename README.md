# Fieldnote / Forest

A full-stack research interface for the Covertype forest-cover classification project in this repository. It keeps the original 54 predictor columns and seven target classes from the comparison notebook, packages a fitted scikit-learn pipeline for local inference, and presents class probabilities in an Angular field workspace.

The interface takes visual cues from forest monitoring and conservation sites: restrained greens, terrain contours, editorial typography, and clear data panels. It does not imply that the U.S. Covertype dataset represents Pakistan.

## Project and model

- **Task:** seven-class forest cover type classification (`Cover_Type` 1–7).
- **Source:** `Covertype_ML_Comparison.ipynb` and the public Forest Cover Type dataset stored in `covertype.zip`.
- **Input:** 54 predictors in the notebook's original order: 10 terrain measurements, 4 wilderness area indicators, and 40 soil type indicators. The target column is never sent as an input.
- **Pipeline:** the notebook's tree preprocessor (median imputation for the 10 numeric fields, most-frequent imputation for the indicators) followed by its Histogram Gradient Boosting classifier.
- **Split:** stratified 80/20 holdout, random state 42. Training metrics are written to `docs/model-metrics.json`.
- **Classes:** 1 Spruce/fir; 2 Lodgepole pine; 3 Ponderosa pine; 4 Cottonwood/willow; 5 Aspen; 6 Douglas-fir; 7 Krummholz.

This is an educational research prototype. Predictions are not a substitute for field surveys, ecological review, or land-management decisions.

## Requirements

- Python 3.14 is installed in the current workspace; Python 3.12 is used in CI. Use a Python version supported by the selected scikit-learn release.
- Node.js 24 LTS or another Angular 22 supported release, and npm 11 or later.
- Git.

Check installed versions with `git --version`, `node --version`, `npm.cmd --version`, `py --version`, and `python -m pip --version`. Angular 22 supports Node 22.22.3, 24.15.0, or 26.0.0 and newer within those major versions. The GitHub workflows use Python 3.12 and Node 24.

## Set up the local model and API

From the repository root in PowerShell:

```powershell
py -3.14 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r backend\requirements.txt
.\.venv\Scripts\python.exe -m backend.make_payload
.\.venv\Scripts\python.exe -m backend.train_model
.\.venv\Scripts\python.exe -m pytest -q backend\tests
.\.venv\Scripts\python.exe -m backend.app
```

The training command reads the supplied dataset archive, performs the notebook's stratified split, fits the configured pipeline, and writes `backend/models/model_bundle.joblib` plus `docs/model-metrics.json`. The generated sample in `data/sample_inputs.csv` and `backend/test_payload.json` contains one public dataset row with the target removed.

Check the API in another terminal:

```powershell
curl.exe --noproxy "*" http://127.0.0.1:5000/health
curl.exe --noproxy "*" http://127.0.0.1:5000/schema
curl.exe --noproxy "*" -X POST http://127.0.0.1:5000/predict -H "Content-Type: application/json" --data-binary "@backend/test_payload.json"
```

`GET /health` reports model readiness; `GET /schema` describes all fields and classes; `POST /predict` validates the full schema and returns the predicted class and probabilities. The API binds to `127.0.0.1` only.

## Run the Angular app

Keep Flask running in Terminal 1. In Terminal 2:

```powershell
cd frontend
npm.cmd ci
npm.cmd start
```

Open `http://localhost:4200`. The Angular development proxy maps `/api/*` to the local Flask server. The sample plot loads the first public dataset observation. The form validates numeric ranges and enforces one selected wilderness area and one selected soil type.

For a production build:

```powershell
npm.cmd run build
```

Production builds are configured as static previews: prediction is disabled because static hosting does not run Flask or load the model.

## GitHub Actions and Pages

`.github/workflows/ci.yml` runs the Flask API tests and Angular production build on pushes and pull requests to `main`. `.github/workflows/pages.yml` listens for completion of that CI workflow and deploys only a successful push to `main`; failed CI runs are skipped. You can also start a Pages deployment manually from **Actions ? Deploy Angular to GitHub Pages ? Run workflow**. The deploy job builds Angular with the repository base path and publishes `frontend/dist/forest-cover/browser`.

The published GitHub Pages site is a static frontend: it cannot run Flask or host the trained model. For predictions, run the Flask API and Angular development server locally using the commands above; the development proxy forwards `/api` requests to Flask. To make inference work for all Pages visitors, deploy Flask and its model bundle to a separate API host, then configure the frontend to call that host and allow the Pages origin in the API's CORS policy.

The repository source is [github.com/ehtishamamjaddev/devops](https://github.com/ehtishamamjaddev/devops). The Pages URL is https://ehtishamamjaddev.github.io/devops/.

## Manual viva workflow

1. Make and save a visible change in VS Code, such as the `<title>` in `frontend/src/index.html`.
2. From the repository root, stage, commit, and push it:

   ```powershell
   git add frontend/src/index.html
   git commit -m "Update page title"
   git push origin main
   ```

3. In GitHub **Actions**, show the **Full-stack CI** run. It must pass the backend tests and Angular build.
4. After CI succeeds for the `main` push, show **Deploy Angular to GitHub Pages** building and deploying the same commit. Open the Pages URL and hard-refresh with Ctrl+F5 to show the change.
5. To demonstrate the backend, start the trained local Flask API and Angular dev server in separate terminals. Check `/health`, then submit the form at `http://localhost:4200`. GitHub Pages itself demonstrates the static frontend; it does not host the Flask inference service.
## Development checks

```powershell
\.venv\Scripts\python.exe -m pytest -q backend\tests
cd frontend
npm.cmd run build
```

For a different trained model, preserve its fitted preprocessing, predictor names/order, target meaning, and supported ranges. Update `backend/schema.py` and `frontend/src/app/feature-schema.ts` together. Never fit a new scaler or preprocessor on one prediction record.
