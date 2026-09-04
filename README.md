# Demo-CI-Pipeline
For the course DD2482, demo showing a CI pipeline

## Shopping list GUI


```sh
python3 -m venv .venv  
# on macOS
source .venv/bin/activate
pip install -r requirements.txt
chmod +x run.sh
./run.sh
```
## The bugs

- **Duplicate check never fires** — `WHERE name = %s` on a `utf8mb4_bin` column is a byte-for-byte comparison, so for instance `Milk` never matches `milk`. Duplicate would be inserted, no ValueError as intended. Fails: `DID NOT RAISE ValueError`
- **Swapped UPDATE parameters** — `(item_id, bought)` into `SET bought = %s WHERE id = %s` writes the wrong value to the wrong row. Fails: `assert 1 in (False, 0)`

## Why the unit tests pass

- Mocks enforce no constraints and apply no collation
- Mocks return what a developer *decided* a database returns