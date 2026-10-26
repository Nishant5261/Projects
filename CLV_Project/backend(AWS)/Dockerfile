FROM python:3.10-slim
WORKDIR /app

# Install the OpenMP C++ library required by LightGBM
RUN apt-get update && apt-get install -y libgomp1 && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

# Document the port the application runs on
EXPOSE 8000

# Set the default command to execute when the container starts
CMD ["uvicorn", "backend:app", "--host", "0.0.0.0", "--port", "8000"]