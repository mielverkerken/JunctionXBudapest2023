# Use an official Node runtime as a parent image
FROM node:16 as builder

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy package.json and package-lock.json (if available) to the working directory
COPY package*.json ./

# Install project dependencies
RUN npm install

# Copy the rest of your app's source code from your host to your image filesystem.
COPY . .

# Build the application - this depends on your scripts in package.json
RUN npm run build

# Production stage
FROM nginx:alpine
COPY --from=builder /usr/src/app/allseek-dashboard-build /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]