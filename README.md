# fast-model-context-protocol

## Setup Steps

1. Install uv, a package and project mennager for Python from Github or from PyPI repository

PyPI:
```bash
pip install uv
```

Github:
[link](https://github.com/astral-sh/uv)

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

This feature will run the local client to acess the local server and execute one of the tools.
No LLM will be used, this feature is designed for *demonstration & troubleshooting*


```bash
uv run main.py api
```

```bash
uv run main.py docker
```

## Running with Gemini CLI
Gemini CLI is a command-line AI workflow tool that leverages the Gemini LLM model to respond to user queries.

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

## Running the Server 

To run the server in SSE mode to connect via the network/internet:
```bash
uv run main.py sse 
```

To run the server in STDIO mode to connect as localhost:
```bash
uv run main.py stdio
```


