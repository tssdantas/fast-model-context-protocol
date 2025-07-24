# fast-model-context-protocol

## Setup Steps

1. Install UV, a package and project menager for Python from Github or PyPI. UV is required to work correctly with Gemini CLI.

Github: [link](https://github.com/astral-sh/uv)

PyPI:
```bash
pip install uv
```

2. Create virtual environment and activate it
```bash
uv venv
.venv\Scripts\activate
```

3. Install dependencies:

```bash
uv add -r requirements.txt
```

## Running local tests

This feature runs the local client against the local server and executes one of the tools automatically. No LLM is used, this is intended for demonstration and troubleshooting.


```bash
uv run main.py api
```

```bash
uv run main.py docker
```

## Running with Gemini CLI
The Gemini CLI is a command‑line AI workflow tool that uses the Gemini LLM model to respond to your prompts.
*Gemini will automatically detect and start the MCP server in the project directory*.

1. Install Gemini CLI from [this](https://github.com/google-gemini/gemini-cli) repository or with NPM:
```bash
npm install -g @google/gemini-cli
```
3. Run this command in this project folder and it will automatically load the seetings in /.gemini
```bash
gemini
```
3. Try these prompts

```gemini
What is the number of publication sources in Japan?
```

```gemini
Show me the distribution of the types of publication sources in Brazil.    
```

```gemini
Use the mainAPIServer MCP to pull the python:3.9-slim image from Docker Hub and run it to display the Python version. Ensure Docker Hub authentication uses the credentials provided in .gemini/settings.json and .env.  
```

The expected outputs can be found in the screenshots in /docs/gemini screenshots/

## Running the Server for other Clients 

To run the server in SSE mode to connect via the network/internet:
```bash
uv run main.py sse 
```

To run the server in STDIO mode to connect as localhost:
```bash
uv run main.py stdio
```


