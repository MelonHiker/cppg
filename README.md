# CPPG - Competitive Programming Problem Generator

## Requirements

- Python 3.12 or higher
- Git LFS

## Installation

1.  **Create and activate a virtual environment:**

    ```console
    python3 -m venv venv
    source ./venv/bin/activate
    ```
2.  **Install dependencies:**

    ```console
    pip install -r requirements.txt
    ```
3.  **Configure API Keys:**

    *   Create a `.secrets.toml` file in the `./src/configs/` directory.
    *   Add your Gemini API keys to the file:

        ```toml
        GEMINI_API_KEY = "YOUR_GEMINI_API_KEY"
        ```

## Running the Application

```console
uvicorn app:app --reload
```
The `--reload` flag enables automatic server restarts upon code changes, which is helpful during development.

The application will be available at http://localhost:8000/

## Observability
This application is instrumented for observability using Phoenix. You can view traces of all calls at: http://localhost:6006/.

You can also visualize the workflow diagrams in the drawing_workflows directory