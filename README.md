# Campus Lost & Found + Grievance Portal

A Django web application that gives a campus a single place to report lost/found items and raise grievances, with status tracking and admin oversight for both.

## Overview

Most campuses handle lost items and grievances informally — WhatsApp groups, notice boards, or emails that go nowhere. This project puts both under one portal with:

- **Lost & Found** — students report lost items or post found items, with basic matching to surface likely pairs, and a claim workflow to hand items back.
- **Grievance Redressal** — students/staff submit grievances (hostel, academic, administrative, etc.) that get routed to the right department and tracked through a defined status workflow (Open → In Review → Resolved/Escalated).
- **Admin Dashboard** — staff can view, assign, and resolve cases from both modules, with basic analytics.
- **Notifications** — email/in-app alerts on matches, status changes, and resolutions.

## Tech Stack

- **Backend:** Django
- **Database:** PostgreSQL (SQLite for local development)
- **Frontend:** Django templates (server-rendered), with room for a DRF API layer later
- **Other:** Docker for containerized setup

## Project Structure

```
campus_portal/
├── config/                  # project settings, root URLs, WSGI/ASGI
│   └── settings/            # base / dev / prod settings split
├── apps/
│   ├── core/                 # shared base models, permissions, mixins
│   ├── accounts/              # custom user model, auth, roles
│   ├── lostfound/              # lost/found reporting + matching
│   ├── grievance/               # grievance submission + status workflow
│   ├── notifications/            # email/in-app alerts
│   └── dashboard/                 # admin/staff case management + analytics
├── templates/                # HTML templates, organized per app
├── static/                    # CSS, JS, images
├── media/                      # user-uploaded files (item photos, attachments)
├── requirements/                # base / dev / prod dependency files
├── docs/                          # ER diagram, API reference, setup notes
└── tests/                          # test suite
```

## Getting Started

> Setup instructions will be filled in once the initial Django project and dependencies are in place.

```bash
# clone the repo
git clone <repo-url>
cd campus_portal

# create and activate a virtual environment
python -m venv venv
source venv/bin/activate

# install dependencies
pip install -r requirements/dev.txt

# apply migrations
python manage.py migrate

# create a superuser
python manage.py createsuperuser

# run the dev server
python manage.py runserver
```

## Roles

| Role | Access |
|---|---|
| Student | Report lost/found items, submit grievances, track own cases |
| Staff | Handle grievances/items assigned to their department |
| Admin | Full dashboard access, manage users, reassign/resolve any case |

## Status

Early stage — project scaffold in place. Core apps, models, and views are being built out incrementally.

## License

TBD