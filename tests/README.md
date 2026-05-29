# Tests

Use this folder for automated tests.

Recommended structure:

```text
tests/
  test_data_harvester.py
  test_data_enricher.py
  test_model_trainer.py
  test_api.py
```

Start with focused unit tests for schema normalization, feature engineering, and prediction output shape.

Current coverage:

- API route registration and response checks
- Schema normalization and data-quality reporting
- Risk scoring
- Anomaly detection

Run:

```powershell
venv\Scripts\python.exe -m pytest
```
