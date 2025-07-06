# Base Python image
FROM python:3.11-slim

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all files
COPY . .

# Expose port for Gradio
EXPOSE 7860

# Run the app
CMD ["python", "app.py"]
