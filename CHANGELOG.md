Changelog
=========

[Unreleased]
------------
- Add a parameter for retrieving the entity attribute from the request instead of request.user #20

[v0.1.0] - 2023-02-06
------------------
- Add a script to generate a Fernet key (#21)
- Add templates for issues and pull requests (#24)
- Add documentation for the package (#10) 

[v0.0.3] - 2023-02-05
------------------

- Bug: Default settings are not loaded in the project (#25) 

[v0.0.2] - 2023-02-04
------------------

- Fix typo on admin `expiry_date` <- `expires_at` (#4)

[v0.0.1] - 2023-02-04
------------------

- Add apikey model (#9)
- Add Django admin to manage API keys (#11)
- Add authentication backend (#12) 
- Add default permissions classes (#13)
- Add creation date field on ApiKey (#14)
- Add package for linting, coverage and syntax checker (#18)