# PHP Diagnostics Server
# Uses official PHP image with Apache for system information display
FROM php:8.3.20-apache

# Copy application code into web root
COPY src/ /var/www/html/  # PHP files served from Apache's default directory

# Expose HTTP port for web access
# Note: Consider restricting access in production
EXPOSE 80  # Standard web port for Apache

