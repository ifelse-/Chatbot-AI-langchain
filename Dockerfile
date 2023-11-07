# Use the official Python 3.11.0 image as the base image
FROM python:3.11.0

# Set the working directory inside the container to /app
WORKDIR /app

# Copy the Pipfile and Pipfile.lock from the host to the container's /app directory
COPY Pipfile Pipfile.lock ./

# Install the pipenv package manager
RUN pip install pipenv

# Generate a requirements.txt file from the pipenv environment
RUN pipenv requirements > requirements.txt

# Install the Python packages specified in the requirements.txt file
RUN pip install -r requirements.txt

# Copy the contents of the host's current directory (.) to the container's /app directory
COPY . ./

EXPOSE 8501

CMD ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]