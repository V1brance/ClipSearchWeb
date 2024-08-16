FROM ubuntu:20.04
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y python3.9 python3-pip

# Set working directory
WORKDIR /hab

# Copy the application code including requirements
COPY ./app /hab

# Install dependencies from within the app directory
RUN pip3 install -r /hab/requirements.txt

# Copy the entrypoint script
COPY ./app/entrypoint.sh /hab/entrypoint.sh

# Ensure the entrypoint script is executable
RUN chmod +x /hab/entrypoint.sh

# Set the entrypoint
ENTRYPOINT ["/hab/entrypoint.sh"]