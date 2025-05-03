# Multi-stage build
FROM composer:2 as composer

WORKDIR /app
COPY src/composer.* ./
RUN composer install --no-dev --no-scripts --no-autoloader

# Final stage
FROM php:8.2-apache

# Install system dependencies and PHP extensions
RUN apt-get update && apt-get install -y \
    curl \
    libpng-dev \
    && docker-php-ext-install opcache \
    && a2enmod rewrite headers \
    && rm -rf /var/lib/apt/lists/*

# Configure PHP and Apache for production
COPY docker/php.ini /usr/local/etc/php/conf.d/app.ini
COPY docker/apache.conf /etc/apache2/conf-available/z-app.conf
RUN a2enconf z-app

# Set recommended PHP.ini settings
RUN { \
    echo 'opcache.memory_consumption=128'; \
    echo 'opcache.interned_strings_buffer=8'; \
    echo 'opcache.max_accelerated_files=4000'; \
    echo 'opcache.revalidate_freq=2'; \
    echo 'opcache.fast_shutdown=1'; \
    echo 'opcache.enable_cli=1'; \
} > /usr/local/etc/php/conf.d/opcache-recommended.ini

# Configure Apache for security
RUN sed -i 's/ServerTokens OS/ServerTokens Prod/' /etc/apache2/conf-available/security.conf \
    && sed -i 's/ServerSignature On/ServerSignature Off/' /etc/apache2/conf-available/security.conf

# Copy application files
COPY src/ /var/www/html/
RUN chown -R www-data:www-data /var/www/html \
    && chmod -R 755 /var/www/html

# Add health check
HEALTHCHECK --interval=30s --timeout=3s \
    CMD curl -f http://localhost/health.php || exit 1

EXPOSE 80

CMD ["apache2-foreground"]

