
# Use an official Python runtime as the base image
FROM python:3.11

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Python scripts into the container
COPY . .

# Set the command to run the Python scripts in the background
CMD ["python", "webhook.py", "&", "python", "main.py", "&"]

