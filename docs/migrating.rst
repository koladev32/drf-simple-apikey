Package Renaming Migration Guide
================================

As part of our efforts to streamline our package offerings, the ``djangorestframework-simple-apikey`` has been renamed to ``drf-simple-apikey``. This section provides a detailed guide on how to migrate your project to use the new package name.

Renaming the Package
--------------------

1. **Uninstall the Old Package**:
   Remove the existing package by running the following command in your terminal:

   .. code-block:: bash

      pip uninstall djangorestframework-simple-apikey

2. **Install the New Package**:
   Install the new package using pip:

   .. code-block:: bash

      pip install drf-simple-apikey

Updating Project Imports
------------------------

You will need to update your import statements in your Django project. Change all existing import statements from:

.. code-block:: python

   import djangorestframework_simple_apikey

to:

.. code-block:: python

   import drf_simple_apikey

Migrating Django Settings
-------------------------

Update your Django project settings to reflect the changes in the package configuration:

- Change any references from ``SIMPLE_API_KEY`` settings to ``DRF_API_KEY``. For example:

  .. code-block:: python

     # Old settings
     SIMPLE_API_KEY = {
         'API_KEY': 'your-api-key-here',
         'OTHER_SETTINGS': 'values'
     }

     # New settings
     DRF_API_KEY = {
         'API_KEY': 'your-api-key-here',
         'OTHER_SETTINGS': 'values'
     }

Ensure that you update these settings throughout your project configuration files to avoid any issues during deployment or development.

Support and Feedback
--------------------

For more information, detailed support, or to provide feedback about the migration process, please visit our documentation site at [New Package Documentation URL](https://example.com/new-package-info) or contact support directly.

We appreciate your cooperation and understanding as we continue to improve our software offerings.
