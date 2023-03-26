Start codespace as per https://datasette.io/tutorials/codespaces

Setup the dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
```

```bash
datasette install \
  datasette-vega \
  datasette-cluster-map \
  datasette-copyable \
  datasette-configure-fts \
  datasette-edit-schema \
  datasette-upload-csvs
```

Initialize the DB:

```bash
./preprocess.py
```

View the DB:

```bash
datasette mmm.db
```

A popup inside codespaces in-browser vscode will ask to open redirected port.


Launch the app:
```bash
uvicorn mmm:app --reload
```

