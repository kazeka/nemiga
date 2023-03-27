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
The script `preprocess.py` accepts a single filename as argument. The default is `data.json`, can also be used as 
`./preprocess.py data_new.json`.


Start Datasette to view SQLite DB:

```bash
datasette mmm.db &
```

A popup inside codespaces web UI will ask to open Datasette at redirected port 8001.


Launch the FastAPI app at default port 8000:
```bash
uvicorn mmm:app --reload &
```

The app provides the following endpoints:
```
/
/docs
/get_level_for/{user_id}
/get_payouts_for/{user_id}
```

More info about the API is available at the `/docs` endpoint.

### Need for clarification
I implemented skipping payouts for users with higher level but lower down the recommendation chain in pairwise manner.
Is this the intention? An alternative would be to look at the chain as a whole.

### Highlights of the implementation
Datasette provides an interface for exploring underlying SQLite DB. FastAPI was chosen for clarity and readability.
NetworkX was chosen to represent the referential tree as directed graph because it provides sophisticated graph API.
Future work includes adding endpoint to extend the referential tree by adding new users at the appropriate nodes, 
testing module, and refactoring (incl. DB).
