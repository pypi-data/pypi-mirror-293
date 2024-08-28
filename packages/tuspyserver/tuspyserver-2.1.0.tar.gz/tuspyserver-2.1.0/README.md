# FastAPI Tus

FastAPI Extension implementing the Tus.io server protocol

### Prerequisites `FastAPI`

## Installation

Installation from PyPi repository (recommended for latest stable release)

```
pip install tuspyserver
```

## Usage

### main.py

```python
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

from tusserver.tus import create_api_router

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/static", StaticFiles(directory="static"), name="static")


def on_upload_complete(file_path: str, metadata: dict):
    print('Upload complete')
    print(file_path)
    print('Upload Metadata')
    print(metadata)


app.include_router(
    create_api_router(
        files_dir='/tmp/different_dir', # OPTIONAL
        max_size=128849018880, # OPTIONAL
        on_upload_complete=on_upload_complete # OPTIONAL
        prefix="files"
    ),
)
```

This package has the ability to upload, download, delete (including a scheduler) files.

```python setup.py sdist bdist_wheel```

Any contribution is welcomed.

<a href="https://www.buymeacoffee.com/edihasaj" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-red.png" alt="Buy Me A Coffee" style="height: 60px !important;width: 217px !important;" ></a>
