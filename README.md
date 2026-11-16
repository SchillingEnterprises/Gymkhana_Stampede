# Gymkhana Stampede

A legacy Django event and Derby experience prototype with checkpoint, event, reward, and location-related concepts, plus a substantial preserved media collection.

## Preserve the project

The repository contains hundreds of original event and archival images. Do not remove the media archive, rewrite historical data, or replace a committed database as part of routine cleanup. Keep source, project assets, and historical context intact unless an individual change has been reviewed.

## Runtime status

This repository began as a Django 2.2-era prototype. The active web runtime is now separated from its old research/notebook/cloud-client dependency collection and targets Django 6.1.3, django-allauth 65.22.1, Python 3.12, Pillow, Gunicorn, and Psycopg 3. The previous oversized requirements list remains in Git history; it is not installed by the active web app. Archived vision samples and the optional EasyAPI upload adapter are not part of the runtime.

## Environment

Copy `.env.example` as a reference and export its values. The application does not automatically read .env files. `DJANGO_SECRET_KEY` is mandatory. `DJANGO_DEBUG` and `DJANGO_ALLOWED_HOSTS` must be set for the target environment.

Local development defaults to SQLite. CI always points at a disposable database. Production must set `DJANGO_DB_ENGINE=postgresql` and configure `DJANGO_DB_NAME`, `DJANGO_DB_USER`, `DJANGO_DB_PASSWORD`, and `DJANGO_DB_HOST` for a persistent PostgreSQL/Cloud SQL instance. Do not deploy the tracked SQLite database as production storage. Browser mapping keys are optional environment variables; restrict replacements to required APIs and known domains. A key previously committed to public history must be rotated, not merely removed from current files.

## Quality checks

The maintenance workflow compiles project Python and runs standard-library security configuration tests. These are early guardrails, not a substitute for running the full application against a supported dependency set and a disposable copy of representative data.

## Production readiness

The framework baseline and App Engine WSGI/runtime declaration are now aligned with supported versions. The app is **not yet production-ready**: provision persistent PostgreSQL/Cloud SQL, configure the Django secret and allowed hosts through a secret manager, configure real email delivery and account verification, validate backups and restore, rehearse migrations against a protected representative-data copy, and test the deployment on the target host. Signup remains disabled until account onboarding is linked to Participant profiles. Do not run migrations against the tracked database.

## Dependency modernization

See [the dependency upgrade review and release gates](docs/dependency-upgrade-review.md) before merging any large package update.

## Participant and checkpoint data model

The original event profile model is renamed in place to `Participant` by a forward migration, preserving the existing participant table and rows. A nullable one-to-one link to Django's authentication account is added, but existing participants are not automatically turned into login accounts. Legacy coordinate strings and proof-file path values are retained; the migration does not geocode coordinates or relocate files.

The checkpoint status field is renamed without changing existing values. New checkpoints default to unapproved (`is_valid=False`) until explicitly reviewed. Event and reward point columns remain ordinary integers so the migration does not introduce database constraints that could reject legacy values. Never run this migration against a production or committed database without a verified backup and representative-data test.


## Web experience and route status

The Django views now have templates in the app's actual `templates/` directory. The older HTML mockups remain preserved under `static/Derby_Event/templates/html/` as source archive material; they are not the templates rendered by Django. The new shared layout uses Bootstrap 5.3.9 with pinned CDN Subresource Integrity, semantic page landmarks, and responsive navigation.

Login and signup routes now delegate to django-allauth rather than displaying static forms that never submitted. The participant-profile workflow is not yet integrated with account signup, and photo submissions, reward awarding, and the leaderboard remain explicitly inactive. Do not present those features as live until their data and moderation flows are implemented and tested.

The Louisville guide preserves the categories and place ideas from the original static archive. It is a starting point, not a live directory: verify current partner status, hours, access, and links before publishing specific recommendations.


## Supported runtime checks

Install the active web dependencies with `python -m pip install -r requirements.txt`. Run the app checks from the repository root:

```bash
export DJANGO_SECRET_KEY="a-long-random-local-secret"
export DJANGO_DEBUG=true
export DJANGO_ALLOWED_HOSTS="localhost,127.0.0.1,testserver"
export DJANGO_DB_ENGINE=sqlite
export DJANGO_DATABASE_NAME="/tmp/gymkhana-dev.sqlite3"
python KDF/manage.py check
python KDF/manage.py makemigrations --check --dry-run
python KDF/manage.py migrate
python KDF/manage.py test Derby_Event
python KDF/manage.py collectstatic --noinput
```

The App Engine configuration now uses the actual `KDF.wsgi:application` entry point and Python 3.12. Before deployment, collect static files and configure Cloud SQL, Secret Manager values, allowed hosts, and HTTPS proxy settings. The runtime deliberately fails closed when PostgreSQL is selected but its connection values are missing.

The original `GeopositionField` migration is represented by a migration-local `CharField` compatibility type. It retains the same varchar(42) storage shape, so the old coordinate strings are not parsed, transformed, or discarded. The obsolete geoposition app is no longer required by the live runtime.
