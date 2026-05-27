# qc-dashboard-app
QC Dashboard reports

## PostgreSQL Data Source

The screen page now reads datasets from PostgreSQL instead of local TSV files.

### 1. Configure environment variables

Copy `.env.example` to `.env` and update credentials if needed.

Required variables:

- `QC_DB_HOST` (default `127.0.0.1`)
- `QC_DB_PORT` (default `5432`)
- `QC_DB_NAME` (default `qc_reports`)
- `QC_DB_SCHEMA` (default `public`)
- `QC_DB_USER` (default `postgres`)
- `QC_DB_PASSWORD` (default empty)

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run one-time TSV import

```bash
python scripts/import_screen_tsv_to_postgres.py
```

Optional flags:

```bash
python scripts/import_screen_tsv_to_postgres.py --schema public --data-dir /path/to/data/screen
```

### 4. Start dashboard

```bash
python src/app.py
```
