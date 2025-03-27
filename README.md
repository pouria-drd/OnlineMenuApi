# OnlineMenuApi

**OnlineMenuApi** is a Django-based API designed to help restaurants and coffee shops manage their online menus. This API allows restaurant owners to create and manage menu categories and products efficiently. Customers can browse menu categories and view product details through a well-structured interface.

## Table of Contents

-   [Features](#features)
-   [Prerequisites](#prerequisites)
-   [Installation](#installation)
-   [Setup](#setup)
-   [Environment Configuration](#environment-configuration)
-   [Usage](#usage)
-   [License](#license

## Features

-   **Restaurant Owners**: Create, update, and delete menu categories and products.
-   **JWT Authentication**: Secure authentication using JSON Web Tokens (JWT).
-   **CORS Support**: Enable integration with frontend applications hosted on different domains.
-   **Debug Toolbar**: Optionally enable Django's Debug Toolbar for development.
-   **Rate Limiting**: Implement throttling to limit the number of API requests per user.
-   **Email Integration**: Send automated emails via SMTP for various activities (e.g., user actions).

## Prerequisites

-   Python 3.12.4+
-   Django 5.1+
-   PostgreSQL (or SQLite for local development)

## Installation

1. **Clone the Repository:**

    ```bash
    git clone https://github.com/pouria-drd/OnlineMenuApi.git
    cd OnlineMenuApi
    ```

2. **Create and Activate a Virtual Environment:**

    ```bash
    python3 -m venv .venv
    source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
    ```

3. **Install Dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Set Up Environment Variables:**

    Create a `.env` file in the project root and add the following:

    ```ini
    # ---------------------------------------------------------------
    # Base URL and Admin URL Configuration
    # ---------------------------------------------------------------

    # Base URL for the API
    BASE_URL=""

    # Admin URL for the API (Typically used to access Django's admin panel)
    ADMIN_URL="admin/"

    # ---------------------------------------------------------------
    # Debugging and Secret Key Configuration
    # ---------------------------------------------------------------

    # Debug mode (True for development, False for production)
    # Set to "True" during development for detailed error messages, and "False" in production for security and performance
    DEBUG="True"

    # Secret key for Django (keep this secure!)
    # This is a critical setting, keep it secret and never expose it publicly
    SECRET_KEY="your_secret_key"

    # Enable Django's debug toolbar (optional)
    # Set to "True" to enable the Django Debug Toolbar for easier debugging during development
    ENABLE_DEBUG_TOOLBAR="True"

    # ---------------------------------------------------------------
    # Time Zone and Localization Configuration
    # ---------------------------------------------------------------

    # Time zone (keep this in sync with your server)
    TIME_ZONE="UTC"

    # Enables timezone-aware datetimes in Django
    # If True, Django will store all timestamps in UTC and convert them to the user's local timezone when needed
    USE_TZ="True"

    # Enables Django's internationalization framework
    # If True, Django will support multiple languages and formats based on locale settings
    USE_I18N="True"

    # ---------------------------------------------------------------
    # Static and Media File Configuration
    # ---------------------------------------------------------------

    # Static files URL and root directory
    # URL where static files will be served from, relative to the site root
    STATIC_URL=static/
    # Path where static files will be stored after collection (useful when deploying)
    STATIC_ROOT=static

    # Media files URL and root directory
    # URL where media files (uploads) will be served from
    MEDIA_URL=/media/
    # Path where media files (uploads) will be stored on the server
    MEDIA_ROOT=media

    # ---------------------------------------------------------------
    # Host and Debugging IPs Configuration
    # ---------------------------------------------------------------

    # Allowed hosts for development (keep it simple)
    # These are the domains or IP addresses that Django will allow requests from
    ALLOWED_HOSTS=localhost,127.0.0.1

    # Internal IPs for Django Debug Toolbar and debugging
    # Defines which IPs can access the debug toolbar
    INTERNAL_IPS=127.0.0.1

    # ---------------------------------------------------------------
    # CORS (Cross-Origin Resource Sharing) Configuration
    # ---------------------------------------------------------------

    # Allow credentials (cookies, HTTP authentication, etc.) in CORS requests
    # Set to "True" if you want to allow credentials (e.g., cookies, HTTP headers) in CORS requests
    CORS_ALLOW_CREDENTIALS=True

    # List of allowed origins (comma-separated) that can make CORS requests to your API
    # CORS_ALLOWED_ORIGINS=https://example.com,https://another-example.com

    # List of allowed origins (comma-separated) that can make CORS requests to your API
    # Set this to the URLs of your frontend application(s)
    CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

    # ---------------------------------------------------------------
    # API Throttling Configuration
    # ---------------------------------------------------------------

    # Throttle rates for API requests
    # Throttling limits the number of requests a user can make in a given period
    USER_THROTTLE_RATE="20/minute"  # Limit authenticated users to 20 requests per minute
    ANON_THROTTLE_RATE="10/minute"  # Limit anonymous users to 10 requests per minute

    # ---------------------------------------------------------------
    # JWT (JSON Web Token) Authentication Settings
    # ---------------------------------------------------------------

    # Access token lifetime in minutes
    # Defines how long the access token will be valid before expiration
    ACCESS_TOKEN_LIFETIME="15"  # The access token will expire after 15 minutes

    # Refresh token lifetime in hours
    # Defines how long the refresh token will be valid
    REFRESH_TOKEN_LIFETIME="24"  # The refresh token will expire after 24 hours

    # ---------------------------------------------------------------
    # Email Settings Configuration
    # ---------------------------------------------------------------

    # Email backend to use for sending emails (default is SMTP)
    EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend

    # SMTP server settings
    # Example: Use your SMTP server host, e.g., Gmail's SMTP server
    EMAIL_HOST=smtp.gmail.com
    # Standard port for TLS (587) or SSL (465)
    EMAIL_PORT=587
    # Use TLS for secure email sending
    EMAIL_USE_TLS=True

    # SMTP credentials
    # Your email account's username (e.g., Gmail or custom SMTP service)
    EMAIL_HOST_USER=your-email@example.com
    # Your email account's password or app-specific password
    EMAIL_HOST_PASSWORD=your-email-password

    # Default "from" email address for sending emails
    # Customize this to match the email address you want to appear as the sender
    DEFAULT_FROM_EMAIL=no-reply@example.com

    # ---------------------------------------------------------------
    # Database Configuration
    # ---------------------------------------------------------------

    # Database connection settings for PostgreSQL
    DB_PORT=5432  # Default PostgreSQL port
    DB_HOST=localhost  # Database server location (localhost for local development)
    DB_USER=user  # Database username
    DB_NAME=database  # Database name
    DB_PASSWORD=password  # Database password

    # ---------------------------------------------------------------
    # Logging Configuration
    # ---------------------------------------------------------------

    # File path for login activity logs (default: login_activity_v1.log)
    LOGIN_LOG_FILE=login_activity_v1.log

    # File path for email activity logs (default: email_activity_v1.log)
    EMAIL_LOG_FILE=email_activity_v1.log
    ```

5. **Run Migrations:**

    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

6. **Create a Superuser:**

    ```bash
    python manage.py createsuperuser
    ```

7. **Run the Development Server:**

    ```bash
    python manage.py runserver
    ```

    Your project should now be running at `http://127.0.0.1:8000/`.

## Deployment

To deploy this project to a production environment:

1. **Set Up a Production Environment:**

    - Set `DEBUG=False` in the `.env` file.
    - Configure a production database.
    - Set up a web server like Gunicorn with Nginx.

2. **Collect Static Files:**

    ```bash
    python manage.py collectstatic
    ```

3. **Apply Migrations:**

    ```bash
    python manage.py migrate
    ```

4. **Run the Application with Gunicorn:**

    ```bash
    gunicorn VandAPI.wsgi:application --bind 0.0.0.0:8000
    ```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

For any inquiries, please contact [pouriadrd@gmail.com](mailto:pouriadrd@gmail.com).
