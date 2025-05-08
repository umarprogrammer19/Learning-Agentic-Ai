# FastAPI "Hello World" Project

Welcome to your first FastAPI project! This is a simple "Hello World" example API built using **FastAPI**.

### **Project Structure**

01-HELLO-WORLD/
│
├── .venv/                 # Virtual environment directory
├── .python-version        # Python version used for this project
├── main.py                # FastAPI application file
├── pyproject.toml         # Project metadata and dependency list
├── README.md              # This README file
├── uv.lock                # Dependency lock file
└── **pycache**/           # Python bytecode files


### **How to Set Up and Run the Project**

#### **Step 1: Set Up Your Virtual Environment**

1. First, make sure you have **UV** installed for managing your dependencies. If you don't have it, you can install it with:

   ```bash
   pip install uv
````

2. Create a virtual environment using **UV**:

   ```bash
   uv venv
   ```

   This will create the virtual environment in the `.venv/` directory.

3. Activate the virtual environment:

   * **On macOS/Linux**:

     ```bash
     source .venv/bin/activate
     ```

   * **On Windows**:

     ```bash
     .venv\Scripts\activate
     ```

#### **Step 2: Install Dependencies**

1. Install **FastAPI** and **Uvicorn** using **UV**:

   ```bash
   uv add "fastapi[standard]"
   ```

   This installs FastAPI, Uvicorn (ASGI server), and **httpx** for testing.

#### **Step 3: Run the Application**

1. Now, you can run the FastAPI application using the following command:

   ```bash
   fastapi dev main.py
   ```

   This will run your application in **development mode** with **automatic reloading**.

   Alternatively, you can also run it using **Uvicorn** directly:

   ```bash
   uv run uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   ```

   This will start the server on `http://localhost:8000`.

#### **Step 4: Access the API**

Once your server is running, you can test your API by opening the following URLs in your browser or API testing tools like **Postman**:

* **Root Path**:
  Go to `http://localhost:8000/` to see the `"Hello World"` message.

  ```json
  {"Hello": "World"}
  ```

* **Item Path**:
  Go to `http://localhost:8000/items/5?q=somequery` to see the response with dynamic path and query parameters.

  ```json
  {"item_id": 5, "q": "somequery"}
  ```

#### **Step 5: Interactive API Documentation**

FastAPI automatically generates interactive documentation for your API. You can access this documentation at:

* **Swagger UI**: Visit `http://localhost:8000/docs`
* **ReDoc**: Visit `http://localhost:8000/redoc`

These tools allow you to interact with your API and test endpoints directly from your browser.

### **FastAPI Code Explanation**

Here’s a quick breakdown of the **main.py** code:

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

* **`@app.get("/")`**: Defines a GET endpoint at the root URL (`/`) that returns a simple "Hello World" message.
* **`@app.get("/items/{item_id}")`**: Defines a GET endpoint that takes a dynamic path parameter `item_id` and an optional query parameter `q`.

### **Next Steps**

After completing this "Hello World" example, you can extend your project by:

* Adding more complex routes.
* Implementing **Pydantic** models for validation.
* Writing unit tests using **pytest**.
* Integrating with the **OpenAI Agents SDK** for agentic functionality.

---

### **Conclusion**

You’ve successfully set up and run your first **FastAPI** project! You can now build more complex APIs and integrate additional tools and libraries as needed. Happy coding!

```

This **README.md** file contains all the necessary instructions for setting up, running, and testing your **FastAPI** "Hello World" project.
```
