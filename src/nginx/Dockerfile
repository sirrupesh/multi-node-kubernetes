# Build stage
FROM node:18-alpine AS builder

WORKDIR /app
COPY src/package*.json ./
RUN npm ci

COPY src/ .
RUN npm run build

# Production stage
FROM nginx:1.25-alpine

# Install curl for healthcheck
RUN apk add --no-cache curl

# Add custom nginx configuration
COPY nginx.conf /etc/nginx/nginx.conf.template

# Create non-root user
RUN addgroup -S nginx && adduser -S nginx -G nginx

# Copy built files from builder stage
COPY --from=builder /app/dist /usr/share/nginx/html

# Use environment variables in nginx config
ENV PORT=80
ENV HOST=0.0.0.0

# Configure nginx with environment variables
CMD ["/bin/sh", "-c", "envsubst '${PORT} ${HOST}' < /etc/nginx/nginx.conf.template > /etc/nginx/nginx.conf && nginx -g 'daemon off;'"]

# Set proper permissions
RUN chown -R nginx:nginx /usr/share/nginx/html && \
    chmod -R 755 /usr/share/nginx/html && \
    chown -R nginx:nginx /var/cache/nginx && \
    chown -R nginx:nginx /var/log/nginx && \
    chown -R nginx:nginx /etc/nginx/conf.d && \
    touch /var/run/nginx.pid && \
    chown -R nginx:nginx /var/run/nginx.pid

# Switch to non-root user
USER nginx

# Add health check
HEALTHCHECK --interval=30s --timeout=3s \
    CMD curl -f http://localhost/ || exit 1

EXPOSE 80