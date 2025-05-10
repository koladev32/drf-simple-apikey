Changelog
=========

[Unreleased]
------------

[v2.2.0] - 2025-05-10
------------------

- Fixed: Admin routes asking for API Keys (#74)
- Adding IP whitelisting and blacklisting (#68)

[v2.1.1] - 2024-12-27
------------------

- Fixed:  DOC errors (#76) 
- Fixed: Additional migration is generated (#73) 

[v2.1.0] - 2024-05-23
------------------

- Add migrating documentation (#62)  

[v2.0.1] - 2024-05-23
------------------

- Renaming package

[v2.0.0] - 2024-05-23
------------------

- Rename project (#56)

[v1.1.1] - 2024-05-23
------------------

- Add Deprecation Warnings for Project Renaming (#58)

[v1.1.0] - 2024-05-23
------------------

- Analytics and Monitoring (#52)

[v1.0.2] - 2023-09-16
------------------

- Fix rotation command

[v1.0.1] - 2023-09-16
------------------

- Configure documentation

[v1.0.0] - 2023-09-16
------------------

- Migrate to Django 4.2 LTS (#46)
- Key rotation (#42)
- Add an example project showcasing how to use the package (#45)

[v0.1.2] - 2023-04-21
------------------
- Add an example project to the package (#29)

- Fixed: DoesNotExist error not related to custom model (#38)

[v0.1.1] - 2023-02-26
------------------

- Minor refactoring (#35)

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
