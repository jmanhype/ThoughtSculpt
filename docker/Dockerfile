# Build stage
FROM python:3.9 as builder
WORKDIR /build
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Final stage
FROM python:3.9-slim
WORKDIR /app

# Copy installed Python packages from the builder stage
COPY --from=builder /usr/local/lib/python3.9/site-packages/ /usr/local/lib/python3.9/site-packages/

# Copy your application code
COPY . /app/

RUN useradd -m myuser && chown -R myuser:myuser /app
USER myuser
CMD ["python", "-m", "uvicorn", "thoughtsculpt.api:app", "--host", "0.0.0.0", "--port", "8000"]