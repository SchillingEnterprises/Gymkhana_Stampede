# Gymkhana Stampede

A legacy Django event and Derby experience prototype with checkpoint, event, reward, and location-related concepts, plus a substantial preserved media collection.

## Preserve the project

The repository contains hundreds of original event and archival images. Do not remove the media archive, rewrite historical data, or replace a committed database as part of routine cleanup. Keep source, project assets, and historical context intact unless an individual change has been reviewed.

## Runtime status

This is a legacy Django 2.2-era application with Google App Engine deployment metadata. Its original pinned dependency set contains many obsolete packages spanning web, cloud, notebook, geospatial, numerical, and machine-learning functionality. It should not be upgraded by simply changing the Django pin: application compatibility, third-party imports, migrations, data formats, and the deployment target need staged validation.

## Environment

Copy `.env.example` as a reference and export its values. The application does not automatically read .env files.

Required: DJANGO_SECRET_KEY, DJANGO_DEBUG, and DJANGO_ALLOWED_HOSTS.

Optional browser mapping keys: GEOPOSITION_GOOGLE_MAPS_API_KEY and GOOGLE_API_KEY. Restrict any replacement key to only the required APIs and known domains. A key previously committed to public history must be rotated, not merely removed from the current file.

## Quality checks

The maintenance workflow compiles project Python and runs standard-library security configuration tests. These are early guardrails, not a substitute for running the full application against a supported dependency set and a disposable copy of representative data.

## Production readiness

Not ready for production until the framework/dependency stack is brought to supported releases, authentication and social-login providers are verified, the App Engine configuration is reconciled with the actual KDF project module, and HTTPS, hosts, database, backups, and API-key controls are tested on the target host.

## Participant and checkpoint data model

The original event profile model is renamed in place to `Participant` by a forward migration, preserving the existing participant table and rows. A nullable one-to-one link to Django's authentication account is added, but existing participants are not automatically turned into login accounts. Legacy coordinate strings and proof-file path values are retained; the migration does not geocode coordinates or relocate files.

The checkpoint status field is renamed without changing existing values. New checkpoints default to unapproved (`is_valid=False`) until explicitly reviewed. Event and reward point columns remain ordinary integers so the migration does not introduce database constraints that could reject legacy values. Never run this migration against a production or committed database without a verified backup and representative-data test.
