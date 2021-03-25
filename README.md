## Shipping Flask

## Table of contents

-   [General info](#general-info)
-   [Technical Details](#technical-details)
-   [Screenshots](#screenshots)
-   [Technologies](#technologies)
-   [Setup](#setup)

## General info

Shipping Flask is a E-commerce website with :

-   Authentication
-   Cart Management
-   Password Reset
-   User Customisation
-   Shop Management
-   Invoice Management

Shipping Flask is using Python Flask with Jinja2 templates and Werkzeug. SQLalchemy interacts as an object-relational mapper with the database.

## Technologies

Project is created with:

-   Python v3.9.0
-   astroid v2.4.1
-   bcrypt v3.2.0
-   blinker v1.4
-   cffi v1.14.5
-   click v7.1.1
-   colorama v0.4.3
-   Flask v1.1.2
-   Flask-Bcrypt v0.7.1
-   Flask-Login v0.5.0
-   Flask-Mail v0.9.1
-   Flask-SQLAlchemy v2.4.1
-   Flask-WTF v0.14.3
-   isort v4.3.21
-   itsdangerous v1.1.0
-   Jinja2 v2.11.2
-   lazy-object-proxy v1.4.3
-   MarkupSafe v1.1.1
-   mccabe v0.6.1
-   pdfkit v0.6.1
-   Pillow v8.1.2
-   pycountry v20.7.3
-   pycparser v2.20
-   pylint v2.5.2
-   six v1.15.0
-   SQLAlchemy v1.3.16
-   toml v0.10.1
-   Werkzeug v1.0.1
-   wrapt v1.12.1
-   WTForms v2.2.1

## Setup

To run this project, clone it and start index.html

### On Windows:

Create Environnement Variable :

```
$ SECRET_KEY = '12345678912345678912345678912312' // input your own 32 digits secret key
$ MAIL_USERNAME = 'address@mail.com'
$ MAIL_PASSWORD = 'mailpassword'
```

In [config.py](./flask_blog/config.py) edit with your mail information

```
$ MAIL_SERVER = 'smtp.mail.com' // replace with your mail server
$ MAIL_PORT = 587 // replace with port
$ MAIL_USE_TLS = True // use TLS Boolean
```

### Import project

```
$ git clone https://github.com/antoineratat/shipping_flask.git
$ py -3 -m venv venv
$ venv\Script\Activate
$ pip install -r requirements.txt
$ cd flask_blog
$ python .\run.py
```

### Initialize Database

site.db SQliteCan be connected to other DB in [config.py](config.py) with **SQLALCHEMY_DATABASE_URI**

```
$ venv\Script\Activate
$ python
$ python
$ from run import db
$ db.create_all()
$ exit()
```

## DB Structure

![DB Structure](https://github.com/antoineratat/shipping_flask/blob/master/tracking_db.png?raw=true)

## Screenshots

### Main Page

![Login Screenshot](https://github.com/antoineratat/ShortURL/blob/master/screenshots/s1.PNG?raw=true)

### Product Management

![Login Screenshot](https://github.com/antoineratat/ShortURL/blob/master/screenshots/s1.PNG?raw=true)

### Cart Management

![Login Screenshot](https://github.com/antoineratat/ShortURL/blob/master/screenshots/s1.PNG?raw=true)

### User Management

![Login Screenshot](https://github.com/antoineratat/ShortURL/blob/master/screenshots/s1.PNG?raw=true)

### Invoice Management

![Login Screenshot](https://github.com/antoineratat/ShortURL/blob/master/screenshots/s1.PNG?raw=true)
