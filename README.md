# NHS Car Rental Service — CIS453 Group 2

Complete editable local prototype using Python, Django, SQLite, Django Templates/HTML/CSS, and Django Admin.

## Windows setup (PowerShell or Command Prompt)

Install Python 3.11 or newer with pip from https://www.python.org/downloads/windows/.
Extract the ZIP, then open a terminal in the Car-Rental-Service folder containing manage.py.

```bat
py -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe manage.py migrate
.venv\Scripts\python.exe manage.py seed_data
.venv\Scripts\python.exe manage.py createsuperuser
.venv\Scripts\python.exe manage.py runserver 127.0.0.1:8000
```

Open http://127.0.0.1:8000/ and register a customer account.
Open http://127.0.0.1:8000/admin/ with your superuser to manage categories, cars, availability, customers, profiles, and bookings.
No default passwords or customer accounts are provided.
Stop the server with Ctrl+C.

If `py` is unavailable, substitute `python` for the first command. Commands use the virtual environment's executable directly, so PowerShell script activation is unnecessary.

To run again after setup:

```bat
.venv\Scripts\python.exe manage.py runserver 127.0.0.1:8000
```

To test:

```bat
.venv\Scripts\python.exe manage.py test --verbosity 2
.venv\Scripts\python.exe manage.py check
.venv\Scripts\python.exe verify_concurrency.py
```

The last command uses a temporary, separate SQLite database and leaves your project database alone.

## Demo walkthrough

1. Register; try a duplicate username/email and observe validation.
2. Log out, then log back in using the normalized lowercase username.
3. Save an optional phone/address under Profile.
4. Explore cars; filter by category, transmission, operational availability, or pickup/return dates.
5. Select an available car, enter future dates, and reserve it.
6. Review the server-calculated days, saved daily rate, and total.
7. Try a declined mock payment, then approve it. Confirmation email text appears in the server terminal.
8. Inspect My bookings; modify future dates and complete mock checkout again.
9. Cancel a future booking; a paid mock booking becomes mock refunded and its dates are released.
10. Use Django Admin to add/edit cars or categories, mark maintenance, and edit/cancel bookings.
11. Try an overlapping reservation; validation rejects it. Adjacent reservations are allowed.

## Rental rules and assumptions

- Dates are calendar dates in America/New_York. Pickup may be today or later; return must be later.
- Rentals use [pickup, return), excluding the return day. Three days at $39/day cost $117.
- Category sets the daily rate. The booking saves a rate snapshot; later category changes do not change existing bookings.
- Overlapping confirmed bookings block the same car, including those awaiting mock payment.
- No automatic expiration for unpaid holds in this prototype; customers cancel future holds or an administrator cancels them.
- Car status is an operational override: available, reserved/blocked, or maintenance. Date-specific reservations do not permanently change car status.
- Without dates, catalog availability refers to operational status. With both dates, it also checks booking conflicts.
- Customers may modify dates or cancel only before pickup day. Car changes require cancelling and making a new reservation.
- A modification recalculates the total using the saved rate and resets mock payment to unpaid. There is no real charge/refund ledger.
- Administrative changes validate date ranges and conflicts. Staff may cancel bookings after pickup as an administrative override.
- Cars/categories with booking references are protected against deletion. Booking deletion is disabled in Admin; use cancellation for history.
- Optional profile stores phone/address. Account name/email are fixed in the customer UI.
- Customers can only see/change their own bookings. State-changing actions use POST and CSRF protection.
- Duplicate account usernames/emails are checked case-insensitively. Self-registration stores lowercase usernames/emails; a unique normalized email registry prevents concurrent duplicate email registration.
- Email uses Django's console backend; it prints messages locally and does not send external email.
- Mock payment collects no card details and charges no money. Production deployment is outside this local prototype's scope.

## Editing and project layout

- `carrental/settings.py`: local settings and SQLite connection.
- `rentals/models.py`: category/car/profile/booking models and business validation.
- `rentals/forms.py`, `views.py`, `urls.py`: customer workflows.
- `rentals/admin.py`: staff administration.
- `rentals/templates/rentals/`: Django templates.
- `rentals/static/rentals/style.css`: responsive styling.
- `rentals/tests.py`: 20 automated functional/integration tests.
- `rentals/management/commands/seed_data.py`: repeatable sample fleet.
- `docs/REQUIREMENTS_AND_CHANGES.md`: provenance, traceability, assumptions.
- `docs/TEST_RESULTS.md`: actual validation evidence.

After changing models, run `manage.py makemigrations`, then `manage.py migrate` using your environment's Python.
Back up db.sqlite3 before schema changes. The ZIP starts without a database; migrations and seed_data create it.
The seed command adds sample cars without overwriting existing records.

## Source and scope

Based on the read-only repository snapshot:
https://github.com/NiravMusunuri/Car-Rental-Servie--CIS-453-Group-2
Commit SHA: 3b03ff3aef6f995dec02ebeeb3d6589ad9cbacc5

The original package names, Category/Car/Booking model foundations, category rates, transmission/status fields, and first two migrations were retained.
No Git commits, pushes, branches, PRs, or remote edits were performed.
The delivered ZIP contains no .git metadata.

The referenced chat's summaries were accessible, but the actual uploaded assignment/report files were not exposed in this session. Alignment is based on those summaries, the explicit requested features, and the repository code. Exact report/rubric compliance should be reviewed against your original documents. This package includes test evidence and a demo guide; it does not invent team contribution/reflection statements.

Django 5.2 LTS is pinned for broad Python compatibility. This is a local development configuration with DEBUG enabled.

## Interface

Responsive catalog with bundled representative vehicle images. The header theme button switches light/dark mode and remembers your choice; the initial theme follows your system preference. Custom cars show a neutral placeholder. Images are AI-generated illustrations, not photographs of actual rental inventory. See docs/IMAGE_ASSETS.md for prompts.

## Add your own car photos

Sign in at /admin/, open Cars, select a car (or Add car), then use Image → Choose file and Save. Your photo appears on the catalog and car detail page. The admin also shows a preview. Use the Clear checkbox and Save to restore the bundled sample image, or the placeholder for custom cars. Django validates that the upload is an image. Uploaded photos are stored in the project media/cars folder; keep that folder when copying or backing up your local project. After updating an existing copy, install requirements and run manage.py migrate before restarting the server.

## Public hosting

See docs/HOSTING.md and render.yaml for the complete Django deployment with persistent SQLite and uploaded photos. Local Windows setup is unchanged. Hosting has been prepared but not published.
