# Use a lightweight Python image based on Alpine Linux
FROM python:3.11.9-alpine

# Add a custom directory to the PATH environment variable
ENV PATH="scripts:${PATH}"

# Copy the requirements file to the container
COPY ./requirements.txt /requirements.txt

# Install necessary build dependencies to compile Python packages
RUN apk add --update --no-cache --virtual .build-deps gcc libc-dev linux-headers

# Install Python dependencies from the requirements file
RUN pip install -r /requirements.txt

# Remove build dependencies to keep the image size small
RUN apk del .build-deps

# Create a directory for the app files
RUN mkdir /app

# Copy all files from the host to the app directory in the container
COPY . /app/

# Set the working directory to /app
WORKDIR /app

# Copy any scripts to the /scripts directory in the container
COPY ./scripts /scripts

# Grant execute permissions to all files in the /scripts directory
RUN chmod +x /scripts/*

# Create directories for media and static files
RUN mkdir -p /vol/web/media
RUN mkdir -p /vol/web/static

# Create a non-root user named 'user' for security purposes
RUN adduser -D user

# Give ownership of the /vol directory to the 'user'
RUN chown -R user:user /vol

# Set directory permissions to be accessible by all users
RUN chmod -R 755 /vol/web

# Switch to the non-root user for running the application
USER user

# Specify the command to run when the container starts
CMD ["entrypoint.sh"]
