# Use a minimal Python image
FROM python:3.9-slim

# Set a generic working directory
WORKDIR /app

# Copy only requirements.txt first to allow Docker caching
COPY requirements.txt .

# Upgrade pip and install dependencies
RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files
COPY . .

# Expose Flask's default port
EXPOSE 5000

# Set the default command to run the app
CMD ["python3", "app.py"]