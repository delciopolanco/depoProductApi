# Use the official Python image as a parent image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Install any needed system packages for building psutil
RUN apt-get update && apt-get install -y gcc python3-dev

# Copy the requirements file into the container at /app
COPY requirements.txt /app/

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . /app/

# Expose the port that the application will run on
EXPOSE 80

# Define the command to run your application using uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
