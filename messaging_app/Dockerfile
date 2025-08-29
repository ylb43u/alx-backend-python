# Use official Python image as base
FROM python:3.10

# Set working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Expose port (change if your app uses a different port)
EXPOSE 8000

# Run the application (update if your entrypoint is different)
CMD ["python", "./manage.py", "runserver"]