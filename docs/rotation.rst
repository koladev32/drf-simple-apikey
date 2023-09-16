==============
API Key Rotation
==============

API Key Rotation is a security mechanism designed to enhance the safety of your API by
periodically changing the cryptographic keys used to encrypt and decrypt API keys.
This process involves a seamless transition from an old key to a new one, ensuring minimal
disruption to your API consumers while increasing security.

This document explains how to activate and configure API Key Rotation in your Django
project using the package, detailing the inner workings of the rotation process.

Key Rotation Overview
---------------------

API Key Rotation in the `rest_framework_simple_api_key` package involves periodically
changing the encryption keys used to secure API keys. During rotation, a new key is introduced,
and both the old and new keys are used for a transition period. This ensures that existing API
keys remain valid while new keys are encrypted with the fresh key.

Activation
----------

Before activating a rotation, ensure to set the rotating Fernet key ``ROTATION_FERNET_SECRET`` in the settings of the package.

To activate API Key Rotation, you can choose one of the following methods:

Using Django Management Command
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Open your terminal.

2. Run the following Django management command to start the key rotation:

   .. code-block:: shell

      python manage.py rotation

   This command initializes the rotation process, creating a rotation object, setting the `is_rotation_enabled` flag to `True`
   in the database.

3. To stop the rotation, execute the following command:

   .. code-block:: shell

      python manage.py rotation --stop

   This command disables the rotation process by setting the `is_rotation_enabled` flag to `False` of the latest rotation object with
    `is_rotation_enabled` to `False`.

Using Django Admin Interface
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Access your Django Admin Interface.

2. Navigate to the "API Key Rotation" section.

3. To activate rotation, create a new rotation entry by clicking the "Add" button to create a new rotation object.

4. To deactivate rotation, edit the rotation entry and set the `is_rotation_enabled` flag to `False`.

How Rotation Works
------------------

API Key Rotation operates through several key phases to ensure a smooth transition while
maintaining the security of your API keys.

Key Rotation Phases
~~~~~~~~~~~~~~~~~~~

1. **Initialization Phase**: Rotation begins when you activate it using the methods mentioned
   above.

2. **Transition Phase**: During this phase, both the old and new keys are active. Existing API
   keys continue to work, and new keys are encrypted using the new key.

3. **Completion Phase**: After a defined period (``ROTATION_PERIOD``), the old key is no longer used. New API keys are
   encrypted exclusively with the new key. For this purpose, you will need to manually interchange values of ``ROTATION_FERNET_SECRET``
   and ``FERNET_SECRET``.

Key Usage During Rotation
~~~~~~~~~~~~~~~~~~~~~~~~~

- **Decryption**: API keys can be decrypted using either the old or new key during the
  transition phase, ensuring that existing keys remain valid.

- **Encryption**: During rotation, new API keys are encrypted using the new key to ensure enhanced
  security.