# Online Coding Editor

## Description

The **Online Coding Editor** is a full-stack web application that allows users to write, run, and test Python code directly in the browser. It supports real-time code execution in a secure Docker environment and interactive terminal-like output. This platform is ideal for coding practice, demonstrations, and learning environments where simplicity and usability are key. The system provides an intuitive code editor with Python syntax highlighting and a separate terminal pane for outputs and inputs.

### Features

* **Real-time Code Execution**: Write and run Python code instantly in the browser.
* **Interactive Input Support**: Accepts multiple lines of user input as if using a terminal.
* **Terminal Output Emulation**: Output appears exactly as it would in a standard terminal, preserving the prompt-response format.
* **CodeMirror Editor Integration**: Enhanced editor experience with syntax highlighting and line numbers.
* **Docker-based Execution**: Code runs in isolated Docker containers for security.
* **Responsive Layout**: Works well on desktops, tablets, and mobile devices.

---

## Prerequisites

Ensure the following tools are installed on your machine:

### 🔧 Backend

* **Python (3.8+)**: Required to run the Django server.
* **pip**: Python package manager.
* **Docker**: Required for running code safely in isolated containers.
* **Virtualenv (optional)**: To isolate dependencies in development.

### 💻 Frontend

* **Node.js (16+)**: JavaScript runtime for the frontend environment.
* **npm**: Node package manager.
* **Vite**: Fast build tool and development server.

---

## Project Structure

```
coding-editor/
├── coding-editor-backend/
│   ├── backend/
│   │   ├── docker/runner/
│   │   │   ├── Dockerfile
│   │   │   └── entrypoint.py
│   │   ├── asgi.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   ├── wsgi.py
│   │   ├── __init__.py
│   ├── core/
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── consumers.py
│   │   ├── migrations
│   │   ├── models.py
│   │   ├── routing.py
│   │   ├── tests.py
│   │   ├── views.py
│   │   ├── __init__.py
│   ├── manage.py
│   └── requirements.txt
├── coding-editor-frontend/
│   ├── public/
│   ├── src/
│   │   ├── assets
│   │   ├── components/
│   │   │   ├── CodeEditor.jsx
│   │   │   └── Terminal.jsx
│   │   ├── App.css
│   │   ├── App.jsx
│   │   ├── index.css
│   │   └── main.jsx
│   ├── index.html
│   ├── eslint.config.js
│   ├── package.json
│   ├── package-lock.json
│   ├── .gitignore
│   └── vite.config.js
├── .gitignore
└── README.md
```

---

## Installation & Setup

### Step 1: Clone the Repository

```bash
git clone https://github.com/himanshu-nagar-official/coding-editor.git
cd coding-editor
```

---

## Backend Setup (Django + Channels + Docker)

### Step 2: Set Up Python Environment

```bash
cd coding-editor-backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### Step 3: Run the Django Server

```bash
daphne backend.asgi:application
```

> 💡 **Make sure Docker Desktop is installed and running** on your machine to enable backend code execution inside containers.
---

## Frontend Setup (React + Vite + CodeMirror)

### Step 4: Install Frontend Dependencies

```bash
cd coding-editor-frontend
npm install
```

### Step 5: Start Development Server

```bash
npm run dev
```

Access the app at: http://localhost:5173/

---

## How to Use

### Writing Code

* Use the code editor to write Python code.
* Supported syntax highlighting via CodeMirror.

### Providing Input

* Enter input (if needed) in the input box below the editor.
* Input must be separated by new lines for each `input()` call.

### Running Code

* Click the “Run” button to execute.
* Output appears in the terminal pane on the right.

---

## Limitations

* **Python-only**: Only supports Python code execution.
* **No live debugging**: No step-by-step execution, just full script execution.
* **Terminal is read-only**: Input cannot be typed directly into the terminal panel.

---

## Conclusion

The **Online Coding Editor** is a modern, web-based code runner built with React, Vite, Django, and Docker. It provides a simple yet powerful experience for users looking to run Python code interactively in the browser. The architecture is clean, modular, and scalable — ideal for learning platforms or live demonstrations.
