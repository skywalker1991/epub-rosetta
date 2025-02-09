FROM node:23.6.1

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY package*.json ./

# Install any needed packages specified in package.json
RUN npm install

# Copy the current directory contents into the container at /app
COPY . .

RUN npm run build

FROM nginx:stable-alpine

# Copy the build output to replace the default nginx contents.
COPY --from=0 /app/dist /usr/share/nginx/html

# Expose port 80
EXPOSE 80


# Start Nginx server
CMD ["nginx", "-g", "daemon off;"]