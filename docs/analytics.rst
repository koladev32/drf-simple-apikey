======================
API Key Analytics Middleware
======================

The API Key Analytics Middleware is a component of the `drf-simple-apikey` package that provides
real-time analytics on API key usage. It records each API request, tracking which endpoints are accessed and how frequently.

API Key Analytics Middleware Usage cases
=====================================

Here is why you can use the  analytics feature in your application:

- **Enhanced Decision Making**: It provides comprehensive data on API usage patterns, enabling better resource management and optimization decisions.

- **Accurate Billing**: You can use it for precise billing by tracking each user's API usage, ensuring customers are billed based on actual usage.

- **Improved Security Oversight**: It monitor API access patterns that can help you quickly detect and respond to unauthorized or suspicious activities.


This page details how to integrate and configure the API Key Analytics Middleware in your Django project,
and explains its operation.

Middleware Overview
-------------------

The `ApiKeyAnalyticsMiddleware` automatically tracks access to different API endpoints by intercepting API requests.
It logs each access in the database, allowing you to monitor API usage and optimize API key allocations.

Setup
-----

To use the `ApiKeyAnalyticsMiddleware`, follow these setup instructions:

1. Ensure the middleware app `drf-simple-apikey.analytics` is included in the ``INSTALLED_APPS`` setting
   of your Django project.

   .. code-block:: python

       INSTALLED_APPS = (
           ...
           "rest_framework",
           "drf_simple_apikey",
           "drf_simple_apikey.analytics",  # Ensure this app is added
       )

2. Add the `ApiKeyAnalyticsMiddleware` to the `MIDDLEWARE` settings in your Django configuration.

   .. code-block:: python

       MIDDLEWARE = [
           ...
           'django.middleware.security.SecurityMiddleware',
           'drf_simple_apikey.analytics.middleware.ApiKeyAnalyticsMiddleware',  # Add the middleware here
           ...
       ]

3. Run the migrate command to create the necessary database tables:

   .. code-block:: shell

      python manage.py migrate drf-simple-apikey_analytics

Activation
----------

The middleware is activated as soon as it is added to the `MIDDLEWARE` list and the project is restarted.
No further actions are required to start collecting data.

How the Middleware Works
------------------------

Once activated, the middleware performs the following functions:

1. **Request Interception**: Upon receiving an API request, the middleware extracts the API key used to authenticate the request.

2. **Endpoint Tracking**: It logs the endpoint accessed by the API key.

3. **Data Storage**: All access data is stored in the `ApiKeyAnalytics` model, which can be queried to retrieve analytics.

Data Access
-----------

To access the analytics data:

1. Use Django's admin interface to view and manage the data collected by the middleware.

2. Access the `ApiKeyAnalytics` model through Django's ORM to perform custom queries or export data for further analysis.


