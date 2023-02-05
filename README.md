# Simple API Key

Simple API Key is an API Key authentication plugin for REST API built with [Django Rest Framework](https://www.django-rest-framework.org/). 

For the full documentation, visit https://djangorestframework-simple-apikey.readthedocs.io/en/latest/.

## Generate a Fernet Key
We've made it easier for you by creating a custom django command to quickly generate a fernet key, which is a crucial component in the 
authentication system. Make sure to keep the key secure and store it as an environment variable in your code. Losing the key will result
in a failure of your authentication system, and if someone else gains access to it, they'll be able to decrypt all of your messages.

To generate the fernet key use the following command:

```python
python manage.py generate_fernet_key
```
or 
```python
django-admin generate_fernet_key
```