Throttling
==========

``APIKeyRateThrottle`` limits how many requests each API key can make per time
window, using DRF's built-in sliding-window cache. The counter is tracked
**per key**, not per user or per IP — two keys belonging to the same user each
get their own independent budget.

Setup
-----

Add ``APIKeyRateThrottle`` to your DRF throttle classes:

.. code-block:: python

    # settings.py
    REST_FRAMEWORK = {
        "DEFAULT_THROTTLE_CLASSES": [
            "drf_simple_apikey.throttling.APIKeyRateThrottle",
        ],
        "DEFAULT_THROTTLE_RATES": {
            "api_key": "100/hour",   # global fallback for all API keys
        },
    }

Or apply it directly to a view or viewset:

.. code-block:: python

    from drf_simple_apikey.throttling import APIKeyRateThrottle
    from rest_framework import viewsets

    class YourViewSet(viewsets.ViewSet):
        throttle_classes = [APIKeyRateThrottle]

Rate resolution order
---------------------

For each request, ``APIKeyRateThrottle`` determines the effective rate like this:

1. **Per-key throttle_rate**: if the authenticating ``APIKey`` row has a
   non-empty ``throttle_rate`` field (e.g. ``"50/hour"``), that rate is used.
2. **Global api_key scope**: if ``throttle_rate`` is empty, the value from
   ``REST_FRAMEWORK["DEFAULT_THROTTLE_RATES"]["api_key"]`` is used.
3. **No throttling**: if neither is set, the request is always allowed.

Requests that were not authenticated with an API key (anonymous requests) are
never counted or blocked by this throttle. Combine it with ``AnonRateThrottle``
if you also want to limit unauthenticated traffic.

Per-key rate override
---------------------

Set a custom rate directly on an individual ``APIKey`` instance. The format
mirrors DRF's ``SimpleRateThrottle``: ``"<count>/<period>"``, where the period is
any string starting with ``s``, ``m``, ``h``, or ``d``:

- ``100/hour``: 100 requests per hour
- ``10/minute``: 10 requests per minute
- ``1/second``: 1 request per second
- ``5000/day``: 5,000 requests per day
- ``""`` (empty): Use the global ``api_key`` rate

.. code-block:: python

    from drf_simple_apikey.models import APIKey

    api_key, key = APIKey.objects.create_api_key(
        entity=user,
        throttle_rate="50/hour",
    )

