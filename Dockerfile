FROM python:3.10-slim-buster

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

# Set environment variables
ENV PORT=8080

# Expose the port the app runs on
EXPOSE ${PORT}

# Command to run the application with gunicorn
CMD gunicorn --bind 0.0.0.0:${PORT} app:app