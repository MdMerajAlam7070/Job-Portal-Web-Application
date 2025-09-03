# Job-Portal-Web-Application
1️⃣ What the project is (1 sentence)

This is just a short description of your project.
Example for your project:

"Job Portal Web Application built with Django where users can register, post jobs, and apply for jobs."

It helps the reviewer quickly understand what your project does.

2️⃣ How to run (exact commands)

This section tells anyone (teacher, recruiter, examiner) how they can run your project on their computer.

Step by step explanation:

python -m venv venv
👉 Creates a virtual environment named venv (to isolate your project’s libraries).

venv\Scripts\activate (Windows)
👉 Activates the virtual environment so you can install/run project dependencies safely.
(On Mac/Linux, it’s source venv/bin/activate).

pip install -r requirements.txt
👉 Installs all the libraries your project needs (like Django, Pillow, etc.) from requirements.txt.

python manage.py migrate
👉 Creates all the database tables (like Users, Jobs, etc.) in db.sqlite3.

python manage.py createsuperuser (optional)
👉 Lets you create an admin account (so you can log in to /admin/ with username + password).

python manage.py runserver
👉 Starts the Django development server.
Then you can open the project in browser at:
http://127.0.0.1:8000/


