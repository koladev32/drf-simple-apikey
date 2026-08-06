Changelog
=========

[Unreleased]
------------
- **Changed:** `APIKeyAuthentication` now inherits from DRF's
  `BaseAuthentication` instead of Django's `BaseBackend`, aligning the
  authentication backend with Django REST Framework's authentication API and
  ensuring compatibility with DRF authentication behavior. (#127)
- Added: Opt-in `ENABLE_PER_KEY_SECRET` setting (default `False`). When enabled,
  new API keys carry a random per-key secret (SHA-256 hash stored, verified with
  a constant-time comparison), checked in addition to Fernet decryption
  succeeding. This means a leaked `FERNET_SECRET` alone is no longer enough to
  forge a working key for an existing entity. Off by default; only affects keys
  created after enabling it; existing keys keep working unchanged. See the
  [Threat Model](https://drf-api-key.koladev.xyz/docs/threat-model) docs.
- Fixed: `reload_api_settings` rebound the module-level `package_settings` name
  to a brand-new object on `DRF_API_KEY` changes instead of reloading the
  existing singleton in place. Every other module holds its own
  `from drf_simple_apikey.settings import package_settings` reference, which
  never saw the rebind — so dynamic settings changes (e.g. via Django's
  `override_settings` in a host project's own tests) were silently ignored
  everywhere except the settings module itself. Now reloads in place via
  `package_settings.reload()`, matching how DRF's own settings object works.
- **Changed (potentially breaking)**: `APIKeyAuthentication` now returns `None`
  instead of raising `NotAuthenticated`/`AuthenticationFailed` when the request
  has no `Authorization` header or uses a different scheme's keyword, matching
  DRF's authenticator contract. This lets it be combined with other
  authentication classes (previously it always hard-rejected the request
  first). **If `APIKeyAuthentication` is your only authentication class and
  you relied on a missing key being rejected automatically, add a permission
  class (e.g. `IsActiveEntity`) to your view** — authentication alone no
  longer enforces that a key was provided; see [Getting Started](https://drf-api-key.koladev.xyz/docs/getting-started#protect-a-view).
- Fixed: `get_rotation_status()` cached a "no active rotation" result forever
  (`timeout=None`), so starting a rotation afterwards had no effect until the
  cache was cleared manually. Starting/stopping a rotation via the management
  command or the admin now invalidates the cache immediately, and the negative
  result is now bounded to 60s as a safety net
- Added: Per-key scopes. `APIKey` now has a `scopes` field, and a new `HasAPIKeyScopes`
  permission class enforces a view's `required_scopes` against the authenticated key.
  Keys without scopes remain unrestricted (backward compatible).
- Changed: `request.auth` set by `APIKeyAuthentication` is now the `APIKey` instance
  instead of the raw key string, matching DRF's convention (e.g. `TokenAuthentication`).
- Changed: Documentation theme updated to shadcn for a modern, professional appearance
- Fixed: Removed the `__init__.py` deprecation warning that incorrectly told users of the
  current `drf-simple-apikey` package to switch away from itself; fixed stale
  `readthedocs.io` links (old package name) across README, CONTRIBUTING, and
  `settings.py` to point at the canonical docs site
- Added: [Threat Model](https://drf-api-key.koladev.xyz/docs/threat-model) documentation
  covering the encrypted-vs-hashed storage trade-off, what a leaked `FERNET_SECRET`
  exposes, and incident-response steps
- Fixed: `SECURITY.md` no longer contains generic template placeholder content
- Changed: Rewrote the quickstart into a full production-ready walkthrough (env-var
  secret, key creation/hand-off, curl example, `request.user`/`request.auth`,
  revocation, and a table of every 403 failure cause and why it's 403 not 401)
- Added: [Comparison](https://drf-api-key.koladev.xyz/docs/comparison) page against
  djangorestframework-api-key, OAuth2, and JWT
- Fixed: Packaging metadata — wheels were built as `py2.py3-none-any` due to a leftover
  `universal = 1` setting; added `Requires-Python`, corrected `keyword` to `keywords`
  (previously silently ignored), and added Django/DRF compatibility classifiers and
  `project_urls`

[v2.4.1] - 2026-01-03
------------------

[v2.4.0] - 2026-01-03
------------------

- Added: Modern documentation site with Fumadocs
  - Migrated from RST/Read the Docs to Next.js/Fumadocs
  - Deployed at https://drf-api-key.koladev.xyz
  - Comprehensive SEO configuration with Open Graph and Twitter Cards
  - Structured data (JSON-LD) for better search engine visibility

[v2.3.1] - 2025-12-27
------------------

- Fixed: Documentation updates and fixes
  - Added Python 3.10-3.13 and Django 4.2.17+/5.x support info to README
  - Added security features and type annotations mention to README
  - Documented bump2version usage in CONTRIBUTING.md
  - Fixed import error in customizing_api_key_model.rst
  - Fixed broken links and typos in documentation
  - Added missing settings documentation (IP_ADDRESS_HEADER, API_KEY_CLASS, ROTATION_PERIOD)

[v2.3.0] - 2025-12-27
------------------

- Added: Comprehensive security hardening (#91)
  - Timing attack protection with constant-time comparisons
  - Fernet key validation with security warnings
  - Input sanitization for analytics endpoint paths
  - HTTPS enforcement (auto-enabled in production)
  - IP address validation with safe proxy header handling
  - Comprehensive audit logging for security events
- Added: Type annotations across the entire codebase (#64)
- Added: Python 3.12 and 3.13 support (#92)
- Updated: Dependencies with security patches (#92)
  - Cryptography: 38.0.4 → 43.0.0
  - Django: 4.2 → 4.2.17,<6.0 (Django 5.x support)
  - DRF: 3.14.0 → 3.15.2
  - Black: 22.3.0 → 24.0.0
- Updated: GitHub Actions to v4/v5 with pip caching (#92)
- Fixed: Admin interface entity field now editable when creating API keys (#78)
- Added: New security settings (ENFORCE_HTTPS, ENABLE_AUDIT_LOGGING, MAX_ENDPOINTS_PER_KEY, MAX_ENDPOINT_LENGTH)
- Added: Comprehensive security documentation

[v2.2.1] - 2025-05-10
------------------

- Fixed: Documentation fixes (#81)

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
