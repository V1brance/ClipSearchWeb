FROM ubuntu:20.04
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y python3.9 python3-pip

# Set working directory
WORKDIR /hab

# Copy the application code including requirements
COPY ./app /hab/app

# Install dependencies from within the app directory
RUN pip3 install -r /hab/app/requirements.txt

# Set the working directory for the application
WORKDIR /hab/app

# Command to run the application
CMD ["gunicorn", "--bind", "0.0.0.0:8888", "--workers", "4", "app:app"]
