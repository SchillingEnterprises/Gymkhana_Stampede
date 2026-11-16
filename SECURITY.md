# Security Policy

## Credential exposure

The historical Django settings file included a Google Maps API key and a Django signing key. The current configuration no longer embeds either value. Because the repository is public, assume historical values in Git history are exposed.

**Required owner action:** revoke/rotate the previously exposed Google API key in Google Cloud Console and restrict any replacement to the exact APIs and HTTP referrers or IP addresses required. Generate a new DJANGO_SECRET_KEY and store it only in the hosting provider's secret manager. Replacing the Django signing key invalidates sessions and signed reset links.

## Current controls

- DEBUG is disabled by default.
- SECRET_KEY is required from DJANGO_SECRET_KEY.
- ALLOWED_HOSTS and CSRF trusted origins are environment-controlled.
- HTTPS redirects and secure session/CSRF cookies default on when DEBUG is false.
- HSTS is configurable but disabled by default until the production HTTPS setup is confirmed.
- Google Maps keys are optional environment variables.
- Do not commit .env files, credentials, database exports, or user data.

## Legacy stack warning

The application still uses a Django 2.2-era dependency stack and older Google App Engine metadata. This patch hardens settings but does not complete the framework, dependency, authentication-provider, or hosting migration.

Report vulnerabilities privately through GitHub's private vulnerability reporting feature when available.
