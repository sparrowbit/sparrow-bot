# Python Image as the base image
ARG PYTHON_VERSION=3.11.3
FROM python:${PYTHON_VERSION}-slim as base

# Install nginx & any other neccessary dependencies
RUN apt-get update && apt_get install -y nginx

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1

# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /app

# Set environment varaible for bot(Bot Token & Signing Secret)
#ENV SLACK_BOT_TOKEN ""
#ENV SLACK_SIGNING_SECRET "" 

# Create a non-privileged user that the app will run under.
# See https://docs.docker.com/develop/develop-images/dockerfile_best-practices/#user
ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser

# WHY ? -> This efficiently installs Python dependencies by taking advantage of Docker's caching mechanisms.
# Download dependencies as a separate step to take advantage of Docker's caching.
# Leverage a cache mount to /root/.cache/pip to speed up subsequent builds.
# Leverage a bind mount to requirements.txt to avoid having to copy them into
# into this layer.

# Docker's cache allows reusing previous build layers, speeding up subsequent builds.
# By using cache mounts for pip's cache directory and binding the requirements.txt file, 
# the installation process can be efficient without copying the entire source.
RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirements.txt,target=requirements.txt \
    python -m pip install -r requirements.txt

# Switch to the non-privileged user(which you create earlier) to run the application.
# It's a security best practice to run applications using the least privilege principle.
# The user context is switched to appuser, reducing the potential impact of security vulnerabilities.
USER appuser

# first copy the the environment file
#COPY .env .

# Copy the source code into the container into the working directory of container that we create earlier.
COPY . .

# configre nginx as a reverse proxy
# Configure Nginx as a reverse proxy
RUN echo "server {
    listen 80;
    server_name localhost;

    location / {
        proxy_pass http://127.0.0.1:3000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}" > /etc/nginx/sites-available/default

# Expose the port that the application listens on.
EXPOSE 80
EXPOSE 3000

# Run the application. In bash shell, first execute source .env to load all env variables and then run the application
CMD ["/bin/bash", "-c", "service nginx start && python app.py"]
