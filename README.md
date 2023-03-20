Start codespace as per https://datasette.io/tutorials/codespaces


```
pipx install -r requirements.txt
```


```
sqlite-utils insert mmm.db users data.json --pk id
```

```
datasette install \
  datasette-vega \
  datasette-cluster-map \
  datasette-copyable \
  datasette-configure-fts \
  datasette-edit-schema \
  datasette-upload-csvs
```