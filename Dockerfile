FROM python:3.12-slim

WORKDIR /app

RUN pip install uv

COPY pyproject.toml uv.lock* ./
RUN uv pip install --system -e .

COPY . .
RUN uv pip install --system -e .

EXPOSE 8000

CMD ["sh", "-c", "clix mcp --transport sse --host 0.0.0.0 --port ${PORT:-8000}"]
