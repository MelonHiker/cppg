# CPPG

## Requirements
- Python 3.12

## Installation
(1) setup a virtual environment：
```console
python3 -m venv venv
source ./venv/bin/activate
```
and install necessary packages:
```console
pip install -r requirements.txt
```
(2) Set API key
```console
echo 'api_key = "your api_key"' > ./src/configs/.secrets.toml
```

## How to Run
```console
uvicorn app:app
```