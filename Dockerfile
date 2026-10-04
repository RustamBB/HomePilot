FROM python:3.12-slim
WORKDIR /app
COPY pyproject.toml ./
RUN pip install --no-cache-dir "mcp>=1.28,<2" "fastapi>=0.115" "uvicorn>=0.30" "httpx>=0.27" "pydantic>=2.7" boto3 strands-agents
COPY packages packages
COPY services services
COPY apps apps
COPY demo demo
COPY scripts scripts
COPY deploy/entrypoint.sh /entrypoint.sh
ENV PYTHONPATH=/app/packages/domain:/app/services/mcp:/app/services/agent:/app/services/api \
    HOMEPILOT_MCP_URL=http://127.0.0.1:8765/mcp PORT=8000
EXPOSE 8000
CMD ["/entrypoint.sh"]
