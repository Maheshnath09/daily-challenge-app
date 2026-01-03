# Frontend Dockerfile for Daily Challenge App
FROM node:18-alpine

# Set working directory
WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy application code
COPY . .

# Set build-time environment variable
ARG NEXT_PUBLIC_API_URL=http://127.0.0.1:8000
ENV NEXT_PUBLIC_API_URL=$NEXT_PUBLIC_API_URL

# Build the application with the env var
RUN npm run build

# Expose port
EXPOSE 3000

# Start the application
CMD ["npm", "start"]

