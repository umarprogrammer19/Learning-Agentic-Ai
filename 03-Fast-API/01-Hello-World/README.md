# FastAPI "Hello World" Project

Welcome to your first FastAPI project! This guide walks you through setting up and running a simple "Hello World" API built with **FastAPI**, a modern, high-performance web framework for Python.

## Project Structure

```
01-HELLO-WORLD/
│
├── .venv/                 # Virtual environment directory
├── .python-version        # Specifies Python version
├── main.py                # FastAPI application entry point
├── pyproject.toml         # Project metadata and dependencies
├── README.md              # This file
├── uv.lock                # Dependency lock file
└── __pycache__/           # Python bytecode cache
```

## Prerequisites

- **Python 3.8+**: Ensure Python is installed. You can download it from [python.org](https://www.python.org/downloads/).
- **UV**: A fast dependency and virtual environment manager. Install it with:
  ```bash
  pip install uv
  ```

## Setup Instructions

### Step 1: Clone the Repository

If you haven't already, clone or download the project to your local machine.

### Step 2: Set Up the Virtual Environment

1. Create a virtual environment using UV:
   ```bash
   uv venv
   ```
   This creates a `.venv/` directory in the project root.

2. Activate the virtual environment:
   - **macOS/Linux**:
     ```bash
     source .venv/bin/activate
     ```
   - **Windows**:
     ```bash
     .venv\Scripts\activate
     ```

### Step 3: Install Dependencies

Install the required dependencies (FastAPI, Uvicorn, and httpx) using UV:
```bash
uv add "fastapi[standard]"
```

This command updates `pyproject.toml` and `uv.lock` with the necessary packages.

### Step 4: Run the Application

Start the FastAPI development server:
```bash
fastapi dev main.py
```

This runs the app in development mode with auto-reload enabled.

Alternatively, use Uvicorn directly:
```bash
uv run uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

The API will be available at `http://localhost:8000`.

## Accessing the API

Once the server is running, test the following endpoints:

- **Root Endpoint**: Visit `http://localhost:8000/` to see:
  ```json
  "Hello World"
  ```

- **Item Endpoint**: Visit `http://localhost:8000/items/5?q=somequery` to see:
  ```json
  {"item_id": 5, "q": "somequery"}
  ```

## Interactive API Documentation

FastAPI provides auto-generated, interactive API documentation:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

Use these interfaces to explore and test your API endpoints directly in the browser.

## Code Overview

The `main.py` file contains the core FastAPI application:

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return "Hello World"

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}
```

- **`@app.get("/")`**: Serves a JSON response with a "Hello World" message at the root URL.
- **`@app.get("/items/{item_id}")`**: Handles a dynamic path parameter `item_id` (integer) and an optional query parameter `q` (string).

## Next Steps

To expand this project, consider:

- Adding more endpoints with complex logic.
- Using **Pydantic** models for request/response validation.
- Writing tests with **pytest** and **httpx**.
- Exploring FastAPI's advanced features like dependency injection or WebSocket support.

## Troubleshooting

- **Port Conflict**: If port 8000 is in use, change the port with `--port <new_port>` in the Uvicorn command.
- **Dependency Issues**: Ensure UV is up-to-date (`pip install --upgrade uv`) and re-run `uv add "fastapi[standard]"`.
- **Virtual Environment**: Verify the virtual environment is activated before running commands.

## Conclusion

Congratulations on setting up your first FastAPI project! You now have a lightweight, functional API ready for further development. For more details, refer to the [FastAPI documentation](https://fastapi.tiangolo.com/).

Happy coding!