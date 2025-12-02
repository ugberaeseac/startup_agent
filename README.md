# Startup Copilot Agent

A modular, extensible AI agent system built using **Google ADK**, featuring persistent session storage, custom tools, and a web-based testing interface.

------------------------------------------------------------------------

## Features

-   **Root + Sub-Agent Architecture**
-   **Persistent Memory** using `DatabaseSessionService`
-   **Tooling Layer**
    -   Web search
    -   BuiltInCodeExecutor
-   **State Management**
    -   Per-session user state
    -   Automatic persistence across conversations
-   **ADK Web UI for testing**
-   **Environment-based Configuration**

------------------------------------------------------------------------

## Built With

-   **Python 3.12**
-   **Google ADK** (Agent Development Kit)
-   **Gemini 2.5 Flash**
-   **SQLite** - persistent session + state storage
-   **FastAPI (ADK built‑in webserver)** for agent testing

------------------------------------------------------------------------

## Memory Architecture

![Memory Flow Diagram](https://i.postimg.cc/sfZHns2W/pic-1.png)

------------------------------------------------------------------------

## Getting Started

### Clone the Repository

    git clone https://github.com/ugberaeseac/startup_agent.git
    cd startup_agent

### Create & Activate Virtual Environment

    python3 -m venv venv
    source venv/bin/activate   # macOS/Linux
    venv\Scripts\activate      # Windows

### Install Dependencies

    pip install -r requirements.txt

### Configure Environment Variables

Copy the template:

    cp .env.example .env

Set your **Google API Key**:

    GOOGLE_API_KEY=your_api_key_here

### Run the Agent (CLI Mode)

    python main.py


## License

MIT License.