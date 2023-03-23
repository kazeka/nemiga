Start codespace as per https://datasette.io/tutorials/codespaces


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

```bash
./preprocess.py
```


```bash
datasette mmm.db
```