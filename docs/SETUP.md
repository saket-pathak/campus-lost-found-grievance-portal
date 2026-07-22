# Setup & Quick-Start Guide

Follow these steps to run the Campus Utility Portal locally.

## Prerequisites
- Python 3.10+
- pip (Python package manager)

## Local Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/saket-pathak/campus-lost-found-grievance-portal.git
   cd campus-lost-found-grievance-portal
   ```

2. **Initialize Environment Variables**
   Copy the template env configuration to a local `.env` file:
   ```bash
   cp .env.example .env
   ```

3. **Install Dependencies**
   It is recommended to use a Python virtual environment:
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On Linux/macOS:
   source venv/bin/activate

   pip install -r requirements/base.txt pytest-django
   ```

4. **Run Migrations**
   Initialize the SQLite database:
   ```bash
   python manage.py migrate
   ```

5. **Create administrative category seeds (Optional but recommended)**
   Launch a shell to create basic grievance categories:
   ```bash
   python manage.py shell -c "from grievance.models import GrievanceCategory; GrievanceCategory.objects.get_or_create(name='Hostel Maintenance', department='Hostels'); GrievanceCategory.objects.get_or_create(name='Academics', department='Academic Registry')"
   ```

6. **Create a Superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run Dev Server**
   ```bash
   python manage.py runserver
   ```
   Access the web interface at `http://127.0.0.1:8000/`.

## Running Tests
Run pytest tests to verify application state:
```bash
pytest
```
