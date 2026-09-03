# Demo-CI-Pipeline
For the course DD2482, demo showing a CI pipeline

## Shopping list GUI

Install the Qt5 dependency and launch the desktop application:

```sh
python3 -m pip install -r requirements.txt
PYTHONPATH=src python3 src/main.py
```

The list is kept in memory while the application is running. Items can be added with a quantity, marked as done, and deleted.
