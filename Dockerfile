FROM python:3.12-slim

WORKDIR /app

# Copy application files
COPY . /app

# Install package
RUN pip install --no-cache-dir -e .

EXPOSE 8000

# Run dashboard web server and cloud API
CMD ["python", "server.py", "8000"]
