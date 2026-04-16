# Use Microsoft's Playwright image which includes Python and browser dependencies
FROM mcr.microsoft.com/playwright/python:v1.49.0-noble

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV NODE_MAJOR 20

# Install system dependencies for OpenCV and FFmpeg
RUN apt-get update && apt-get install -y \
    curl \
    gnupg \
    ffmpeg \
    libgl1 \
    libglib2.0-0 \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# Install Node.js
RUN mkdir -p /etc/apt/keyrings /etc/apt/sources.list.d \
    && curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key | gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg \
    && echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_$NODE_MAJOR.x nodistro main" | tee /etc/apt/sources.list.d/nodesource.list \
    && apt-get update && apt-get install nodejs -y

# Install Bun
RUN curl -fsSL https://bun.sh/install | bash
ENV PATH="/root/.bun/bin:${PATH}"

WORKDIR /app

# Copy requirement files first for better caching
COPY requirements.txt package.json ./

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt
RUN npm install

# Optional: Install gstack dependencies if the directory exists
COPY ["~", "./~"]
RUN if [ -d "./~/gstack" ]; then \
        cd "./~/gstack" && bun install; \
    fi

# Copy the rest of the workspace
COPY . .

# Set permissions for any scripts if they exist
RUN chmod +x scripts/*.sh 2>/dev/null || true

# Default command: run the dev script from package.json
CMD ["npm", "run", "dev"]
