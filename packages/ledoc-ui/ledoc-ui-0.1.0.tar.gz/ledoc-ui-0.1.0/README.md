# Ledoc_ui

This package only contains static files for ledoc_ui as a bundle.

It is intended to be used as a python package dependency for any webserver that serves UI for `openapi.json`.

As long as the `openapi.json` in standard format is served at `/openapi.json` path, the UI will work out of the box at `/ledoc`.

## Getting Started

You can import the `ledoc_ui_path` from the package:

```python
from ledoc_ui import ledoc_ui_path
```

And use it in your webserver to serve the UI. For example, in FastAPI:

```python
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI()

...

app.mount(
  "/ledoc",
  StaticFiles(directory=ledoc_ui_path, html=True),
  name="ledoc",
)

...
```

## License

This project is licensed under the MIT License.
