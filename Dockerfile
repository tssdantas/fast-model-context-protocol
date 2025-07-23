FROM python:3.12-slim

WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install dependencies using uv
RUN pip install uv
RUN uv venv
RUN uv pip install -r requirements.txt

# Copy application code
COPY main.py .
COPY .env .
COPY ./src/mcpserver.py src/.
COPY ./src/client.py src/.

# Expose the port the server runs on
EXPOSE 8000

# Command to run the server
CMD ["uv", "run", "main.py", "stdio"] 