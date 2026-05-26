FROM python:3.12-slim

WORKDIR /app

RUN pip install uv

COPY . .
RUN uv pip install --system .

EXPOSE 8000

CMD ["sh", "-c", "clix mcp --transport streamable-http --host 0.0.0.0 --port ${PORT:-8000}"]
