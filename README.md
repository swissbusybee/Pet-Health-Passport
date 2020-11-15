python3 -m venv venv
source venv/bin/activate
python manage.py makemigrations
python manage.py migrate
python manage.py runserver

Clear Existing Data from database:
python manage.py flush

Recreate Superuser:
python manage.py createsuperuser

Load Seed Data:
python manage.py loaddata app/fixtures/profile-data.json
python manage.py loaddata app/fixtures/vaccine-data.json
python manage.py loaddata app/fixtures/immunization-data.json
python manage.py runserver

Run script:
python manage.py runscript send_alert_email
