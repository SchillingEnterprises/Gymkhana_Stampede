# Dependency upgrade review and release gates

## Current baseline

The event application is a Django 2.2.10-era project. The checked-in `requirements.txt` is a historical, very broad pin set spanning the web application, social authentication, geospatial integrations, Google Cloud SDKs, Jupyter/notebook tooling, numerical packages, and TensorFlow. The repository does not currently prove that every pinned package is imported by the deployed event application.

The current `.github/workflows/source-quality.yml` compiles Python and runs source-level security/configuration tests. It does **not** install the full requirements file, run `pip check`, start Django, run the migration graph against a disposable database, or test the App Engine deployment package. A green run therefore does not establish compatibility for large dependency jumps.

## Open package-only upgrades: hold pending compatibility work

The following open Dependabot changes must not be merged solely because dependency review or source compilation is green:

| PR | Package change | Release gate |
|---|---|---|
| #78 | Tornado 5.1 → 6.6.1 | Confirm Jupyter/notebook and any application integration compatibility |
| #74 | TensorFlow 1.15 → 2.21.0 | Prove TensorFlow is an active runtime dependency; if retained, port and test model/API code and compatible protobuf/numpy stack |
| #73 | protobuf 3.6.0 → 7.36.2 | Resolve constraints across legacy Google Cloud clients, TensorFlow, and gRPC |
| #72 | Django 2.2.10 → 6.1.3 | Full framework migration: allauth, middleware, URL routing, model fields, templates, forms, migrations, authentication, and supported Python runtime |
| #70 | IPython 6.4.0 → 9.18.1 | Establish whether interactive tooling is a maintained deliverable; verify Jupyter stack if retained |
| #67 | NumPy 1.15.0 → 2.5.4 | Test all scientific/image/ML consumers and binary wheels; major ABI/API compatibility review |
| #66 | nbconvert 5.3.1 → 7.17.2 | Upgrade and test the complete notebook/nbformat/Jupyter toolchain if used |
| #65 | Dask 0.18.2 → 2026.8.0 | Establish active use and test distributed/data APIs if retained |
| #64 | Notebook 5.7.8 → 7.6.5 | Major notebook architecture/configuration changes; test actual notebooks and extensions if present |
| #63 | Mistune 0.8.3 → 3.4.0 | Check nbconvert/Markdown rendering integration and any direct imports |
| #62 | Werkzeug 0.15.3 → 3.1.9 | Check Flask and any Werkzeug APIs/extensions before updating |
| #61 | urllib3 1.24.2 → 2.8.0 | Resolve compatibility with old requests, botocore, Google clients, and all transitive consumers |

These are package proposals, not verified application upgrades. Keep them open until the corresponding release gate is satisfied; do not consolidate their version pins into `master` as a batch.

## Recommended modernization sequence

1. **Inventory actual runtime imports.** Trace imports from `KDF/KDF`, `Derby_Event`, the WSGI entry point, templates, scheduled tasks, and deployment metadata. Distinguish live application dependencies from archived notebook, machine-learning, and historical SDK dependencies.
2. **Separate dependency groups.** Build a small web-runtime requirements set and separate optional archive/research/notebook extras only where real maintained use is demonstrated. Do not delete archival code or notebooks as a side effect.
3. **Choose a supported Django target.** Upgrade Django with a compatible allauth release and required middleware/settings changes. Stage this independently from unrelated scientific package updates.
4. **Reconcile deployment configuration.** Confirm the App Engine entry point uses the actual `KDF.wsgi` module, then validate the full package on the intended host/runtime.
5. **Add runtime CI.** Install the selected requirements, run `pip check`, Django system checks, URL/view tests, authentication tests, and migrations against a disposable database. Keep the committed database untouched.
6. **Rehearse data migrations.** Use a protected copy with representative historical participant, checkpoint, event, reward, and media references. Verify row counts and foreign-key relationships before and after each migration.
7. **Upgrade one compatible family at a time.** Merge a package update only when the app-level tests and deployment smoke test pass, not merely the dependency scanner.

## Data and security safeguards

- Never run migrations against the tracked database as part of CI.
- Keep original event photos and research assets intact.
- Do not infer that the participant profile is an authentication account; the new nullable relation is intentionally additive.
- New checkpoints remain unapproved by default.
- Rotate any API keys previously committed to public Git history. Moving a key to environment configuration does not revoke its old value.
- Keep secrets out of repository files and restrict browser mapping keys by referrer and API.

## Current disposition

The open upgrades listed above remain **held for application compatibility review**. The participant model and reward calculation repairs already merged to `master` are schema/domain foundations, not a substitute for a supported Django runtime or a representative-data migration rehearsal.
