FROM nginx:alpine

# Set up Alpine package repositories
RUN echo "https://dl-cdn.alpinelinux.org/alpine/latest-stable/main" > /etc/apk/repositories && \
    echo "https://dl-cdn.alpinelinux.org/alpine/latest-stable/community" >> /etc/apk/repositories && \
    apk update

# Install Python and pip
RUN apk add --no-cache python3 py3-pip

# Create a virtual environment and install Flask, Requests, and urllib3
RUN python3 -m venv /app/venv && \
    /app/venv/bin/pip install --no-cache-dir flask requests urllib3

# Copy Nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy application files
COPY app /app
COPY usr/share/nginx/html /usr/share/nginx/html

# Expose port 80
EXPOSE 80

# Start Nginx and Flask using the virtual environment
CMD ["sh", "-c", "/app/venv/bin/python3 /app/app.py & nginx -g 'daemon off;'"]