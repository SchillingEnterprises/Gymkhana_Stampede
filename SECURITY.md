# Security Policy

## Credential exposure

The historical Django settings file included a Google Maps API key and a Django signing key. The current configuration no longer embeds either value. Because the repository is public, assume historical values in Git history are exposed.

**Required owner action:** revoke/rotate the previously exposed Google API key in Google Cloud Console and restrict any replacement to the exact APIs and HTTP referrers or IP addresses required. Generate a new `DJANGO_SECRET_KEY` with `python -c 'import secrets; print(secrets.token_urlsafe(64))'` and store it only in the hosting provider's secret manager. Replacing the Django signing key invalidates sessions and signed reset links.

## Current runtime and controls

The active application runtime has been migrated from the legacy Django 2.2-era stack to Django 6.1.3 on Python 3.12. The old dependency and research snapshots remain historical material; they are not the active web runtime.

Current security controls include:

- `DEBUG` is disabled by default.
- SQLite is allowed only when `DJANGO_DEBUG=true`; a non-debug process must select PostgreSQL and provide database name, user, password, and host.
- PostgreSQL TLS must verify the server certificate: `DJANGO_DB_SSLMODE` defaults to `verify-full` and accepts only `verify-ca` or `verify-full`. Use `DJANGO_DB_SSLROOTCERT` for a private provider CA bundle when required.
- `DJANGO_SECRET_KEY` is required, must be at least 50 characters with at least 5 distinct characters, and must be generated uniquely for each environment.
- `ALLOWED_HOSTS` and CSRF trusted origins are environment-controlled.
- HTTPS redirects and secure session/CSRF cookies default on when `DEBUG` is false.
- HSTS remains configurable but disabled by default until the production HTTPS setup is confirmed.
- Google Maps keys are optional environment variables and must be restricted to the required APIs and origins.
- Public signup remains disabled until participant-profile onboarding and verified email delivery are implemented.
- Do not commit `.env` files, credentials, database exports, or user data.

## Production and deployment boundary

The supported framework baseline does not mean the application is production-ready. Before launch, provision persistent PostgreSQL/Cloud SQL, configure secrets and allowed hosts through a secret manager, configure real email delivery and account verification, validate backups and restore, rehearse migrations against a protected representative-data copy, and test deployment on the target host. The application now rejects SQLite whenever `DJANGO_DEBUG=false`; PostgreSQL must be configured with certificate-verifying TLS. Store database credentials and any provider CA path in the deployment environment or secret manager, not in this repository.

Never run migrations against the tracked SQLite database or production records without a verified backup and reviewed migration plan. Signup, photo submissions, reward awarding, and leaderboard features remain inactive until their account, data, and moderation flows are implemented and tested.

## Historical data and migration safety

The original event media archive and existing participant records must be preserved. The participant model migration is designed to retain the existing participant table and rows; it does not automatically convert participants into login accounts. Legacy coordinate strings and proof-file paths are retained without geocoding or relocation. Validate any future schema change against a disposable, representative copy before deployment.

Report vulnerabilities privately through GitHub's private vulnerability reporting feature when available.
