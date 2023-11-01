# Requirements
1. Docker
2. Docker compose
3. Postman


# Project setup

1. Build the Docker containers for your Django project:
   ```bash
   docker-compose build
   ```

2. Start your Django project and its dependencies with Docker Compose:
   ```bash
   docker-compose up
   ```
   Your Django project should now be up and running.


3. To access the container's shell, open a new terminal window and use the following command:
   ```bash
   docker exec -it finbox-up /bin/bash
   ```
4. Inside the container, create database migrations:
   ```bash
   python manage.py makemigrations
   ```
   This command generates database migration files based on the changes you made to your models.

5. Apply the database migrations to update the database schema:
   ```bash
   python manage.py migrate
   ```
   This step ensures that the database schema matches your Django models.

6. Load initial data from a fixture (JSON file) into the database. Replace core/fixtures/stone.json with the path to your fixture file:
   ```bash
   python manage.py loaddata core/fixtures/stone.json
   ```
   This command populates the database with initial data defined in the fixture.


You can import the Finbox.postman_collection.json in your Postman to access the APIs.
