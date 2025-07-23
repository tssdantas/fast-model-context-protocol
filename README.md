# fast-model-context-protocol

## Setup Steps

1. Install Miniconda, activate it


2. Create virtual environment and activate it
```bash
conda create --name mcp python=3.12
activate mcp
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

## Running local tests

This feature will run the local client to acess the local server and execute one of the tools.
No LLM will be used, this feature is designed for *demonstration & troubleshooting*


```bash
python main.py api
```

```bash
python main.py docker
```

## Running with Gemini CLI
Gemini CLI is a command-line AI workflow tool that leverages the Gemini LLM model to respond to user queries.

1. Install Gemini CLI from [this](https://github.com/google-gemini/gemini-cli) repository or with NPM
2. Run this command in this project folder and it will automatically load the seetings in /.gemini
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
python main.py sse 
```

To run the server in STDIO mode to connect as localhost:
```bash
python main.py stdio
```


