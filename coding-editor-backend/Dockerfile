# 1. Base Image
# Using an official Python image
FROM python:3.9-slim

# 2. Set Environment Variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# 3. Install System Dependencies & Docker CLI
# - ca-certificates, curl: for securely downloading Docker's GPG key
# - docker-ce-cli: the official Docker Command Line Interface
RUN apt-get update && apt-get install -y --no-install-recommends \
ca-certificates \
curl \
&& rm -rf /var/lib/apt/lists/*

# Add Docker's official GPG key
RUN install -m 0755 -d /etc/apt/keyrings
RUN curl -fsSL https://download.docker.com/linux/debian/gpg -o /etc/apt/keyrings/docker.asc
RUN chmod a+r /etc/apt/keyrings/docker.asc

# Add the Docker repository to Apt sources
RUN echo \
"deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/debian \
$(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
tee /etc/apt/sources.list.d/docker.list > /dev/null
RUN apt-get update

# Install Docker CLI
# We only need the CLI, not the full engine, for the DooD approach
RUN apt-get install -y --no-install-recommends docker-ce-cli && rm -rf /var/lib/apt/lists/*

# 4. Set Working Directory
WORKDIR /app

# 5. Install Python Dependencies
# Copy requirements.txt first to leverage Docker layer caching
COPY requirements.txt /app/
RUN pip install -r requirements.txt

# 6. Copy Application Code
# This assumes your Dockerfile is in the 'coding-editor-backend' directory
COPY . /app/

# 7. Expose Port
# The port your Daphne server will run on
EXPOSE 8000

# 8. Set Default Command
# This will run your Django Channels application using Daphne
# It refers to 'backend.asgi:application' from your asgi.py file
CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "backend.asgi:application"]