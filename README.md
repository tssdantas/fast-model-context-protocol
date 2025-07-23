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


## Running the Server

To run the server in SSE mode to connect via the network/internet:
```bash
python main.py sse 
```

To run the server in STDIO mode to connect as localhost:
```bash
python main.py stdio
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
