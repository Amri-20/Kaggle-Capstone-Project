FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install uv for fast dependency management
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin/:${PATH}"

# Copy dependencies
COPY requirements.txt .

# Install dependencies
RUN uv pip install --system -r requirements.txt

# Copy project files
COPY backend/ ./backend/

EXPOSE 8000

ENV DATABASE_URL="sqlite:///./boardroom.db"
ENV HOST="0.0.0.0"
ENV PORT="8000"

CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
