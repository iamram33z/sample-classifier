# Base image with Python 3.12
FROM python:3.12-slim

# Set working directory in the container
WORKDIR /app

# Copy the application code into the container
COPY . .

# Copy the requirements file into the container
COPY requirements.txt ./

# Install dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Expose the port your Flask app runs on
EXPOSE 5000

# Set environment variables for Flask
ENV FLASK_APP=app/flask_app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_ENV=production

# Command to run the application
CMD ["flask", "run"]