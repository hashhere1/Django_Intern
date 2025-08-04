### What is Django?

Django is a **high-level Python web framework** that allows developers to build secure, maintainable websites quickly. It follows the **"batteries-included" philosophy**, meaning it comes with a wide range of built-in features such as authentication, admin panel, ORM (Object-Relational Mapping), form handling, and more.

Django is built on the **MVC (Model-View-Controller)** pattern, although in Django it's referred to as **MTV (Model-Template-View)**:
- **Model** – Defines the data structure and interacts with the database.
- **Template** – Defines how data is presented to the user (HTML pages).
- **View** – Contains the logic to process requests and return responses.

#### Key Features of Django:
- **Rapid Development**: You can build web apps quickly with Django’s built-in tools.
- **Security**: Protects against common attacks like SQL injection, XSS, CSRF, etc.
- **Scalability**: Used by big platforms like Instagram and Pinterest.
- **Admin Interface**: Comes with a powerful, auto-generated admin panel for managing content.
- **ORM**: Lets you interact with the database using Python code instead of SQL.

---
# Daily Progress Report

## Date: August 4, 2025

### Topics Covered
- Introduction to Django
- Understanding Django apps and their role in project structure
- Basic Django commands and project navigation

###  Tasks Completed

- **Learned the basics of Django**  

- **Created three Django apps:**
  - `playground`
  - `store`
  - `tags`

  > *In Django, an app is a Python package that contains a specific functionality (e.g., a blog, a store). A project can contain multiple apps. e.g. a component in website is an app*

- **Installed and configured `django-debug-toolbar`**  
  This is a powerful tool for developers that shows detailed debug information right in your browser. It helps with analyzing SQL queries, cache usage, template rendering time, and more.

- **Updated project `settings.py`**
  - Added the new apps to `INSTALLED_APPS`
  - Configured settings required for `django-debug-toolbar` to work properly

- **Created models in the `store` app:**
  - `Product` – Represents an item available for sale, typically includes fields like name, price, and description.
  - `Customer` – Represents a user or buyer, with fields like name and contact details.
  - `Order` – Represents a purchase record, connecting customers and products with details like quantity and date.

  > *In Django, models are Python classes that define the structure of your database tables. Each model maps to a single table. e.g. a whole website is a project*

- **Learned and practiced basic Django commands:**
  - `django-admin startproject` – To create a new Django project
  - `python manage.py startapp` – To create a new app within a Django project
  - `python manage.py makemigrations` – To create new database migrations based on model changes
  - `python manage.py migrate` – To apply migrations and create/update database tables
  - `python manage.py runserver` – To start the development server
  - `python manage.py shell` – To open an interactive shell with project context

### Skills Learned
- How Django projects and apps are organized
- Writing Django models and understanding their relationship with databases
- Using `django-debug-toolbar` for better development insights
- Executing common Django commands to manage apps and data

### Tools Used
- Django (Python web framework)
- django-debug-toolbar (debugging utility)

---


