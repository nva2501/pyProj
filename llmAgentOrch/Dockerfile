# Use the official Python image with the desired version
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY llmAgentOrch/ ./llmAgentOrch/

# Expose the port that the application will run on
EXPOSE 8000

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Command to run the application
CMD ["uvicorn", "llmAgentOrch.main:app", "--host", "0.0.0.0", "--port", "8000"]
