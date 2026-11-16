# Dependency modernization and release gates

## Active web runtime

PR #86 replaced the old monolithic requirements file with a deliberately small supported web runtime:

| Component | Active version | Purpose |
|---|---:|---|
| Python | 3.12 | Supported application runtime |
| Django | 6.1.3 | Web framework |
| django-allauth | 65.22.1 | Local account login and account routes |
| Pillow | 13.0.0 | Django ImageField support |
| Gunicorn | 23.0.0 | WSGI server |
| Psycopg | 3.3.9 | PostgreSQL driver |

The old requirements set mixed web runtime dependencies with unused notebook, scientific/ML, geospatial, and historical cloud SDK packages. Those packages were not imported by the active event views/models. They are not installed in the active runtime; the previous pin list remains available in Git history.

The App Engine configuration now uses Python 3.12 and the real `KDF.wsgi:application` entry point. The application supports local SQLite and environment-configured PostgreSQL. CI always uses a disposable SQLite database.

## Runtime verification

The existing source-quality workflow now performs real runtime checks:

1. Install `requirements.txt` and run `pip check`.
2. Compile project Python and run source-level security/architecture tests.
3. Run Django system checks.
4. Run `makemigrations --check --dry-run`.
5. Apply migrations to a disposable SQLite database.
6. Run Django integration tests for the public pages and allauth account redirects.
7. Collect static assets.

The old package-only Dependabot proposals #61–#67, #70, #72–#74, and #78 were closed as superseded by the runtime separation. They are not active web dependencies, so merging their individual upgrades would reintroduce unnecessary packages.

## What is still not production-ready

- Public signup remains disabled until account creation is integrated with the `Participant` profile and a real verified-email delivery flow.
- Existing participant rows are not automatically converted into Django authentication accounts.
- Photo submissions, point awarding, and the leaderboard are not implemented as working application flows.
- The app still needs a provisioned persistent PostgreSQL/Cloud SQL instance, Secret Manager configuration, real email delivery, host/CSRF settings, backup/restore verification, and a production deployment rehearsal.
- Do not deploy using the tracked SQLite database or run migrations against it.

## Migration and data safeguards

- The original coordinate field stored text in a varchar(42). The migration-local compatibility field preserves that representation without installing the obsolete geoposition app. No geocoding or coordinate transformation occurs.
- The Participant profile rename is in-place and retains existing rows. Its account link is nullable.
- New checkpoints default to unapproved (`is_valid=False`).
- Reward totals remain integers until historic data has been audited.
- Never run migrations against the tracked database as part of CI. Rehearse on a protected representative copy and compare row counts, foreign keys, file paths, and reward totals.
- Keep original event photos and research assets intact.
- Rotate any API keys previously committed to public Git history. Moving a key to environment configuration does not revoke its old value.
- Keep secrets out of repository files and restrict browser mapping keys by referrer and API.
