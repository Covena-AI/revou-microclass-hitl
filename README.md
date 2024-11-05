# HITL (Human-In-The-Loop) Assistant

A personal assistant that uses LangChain and OpenAI to help schedule meetings and perform other tasks, with human approval required before executing actions.

## Features

- Schedule meetings via Google Calendar
- Human approval workflow for all actions
- Natural language interaction

## Installation

1. Clone the repository

```
git clone <your-repository-url>
cd hitl
```

2. Create and activate a virtual environment

```
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

3. Install dependencies

```
pip install -r requirements.txt
```

4. Create a .env file in the root directory from .env.example
5. Create a credentials.json file from Google Cloud Console

## Running the Application

1. Make sure your virtual environment is activated
2. Run the application:

```
python run.py
```

3. Interact with the assistant through the command line interface
4. Type 'exit' to end the conversation
