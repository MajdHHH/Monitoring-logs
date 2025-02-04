# Use an official Python runtime as a parent image
FROM python:3.9-slim
RUN pip install --no-cache-dir -r requirements.txt

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install psutil (dependency for your app)
RUN pip install --no-cache-dir psutil

# Create log directory
RUN mkdir -p /app/logs

# Run Monitoring-logs.py when the container launches
CMD ["python", "Monitoring-logs.py"]
