# Tau-Factor
## _Tel-Aviv University (non-official) courses and grades repository_

Tau-Factor is a grades repository website of Tel-Aviv University (non-official) courses.


## Features

- REST API implemented using Django python framework
- Frontend using JQuery
- Existing Database with current grades repository can be provided by contacting <factor.tau@gmail.com>

## Installation

Tau-Factor was tested using [Python3.6](https://www.python.org/downloads/release/python-3613/) v1+ to run.

Install the dependencies and devDependencies and start the server:

```sh
python3 -m virtualenv venv
pip3 install -r requirements.txt
cd tau_factor
python manage.py runserver
```

For production environments:
1. Edit ```tau_factor/tau_factor/settings.py```:
1.1 Import evironment instead of development_evnironment.
2. Edit ```tau_factor/tau_factor/enviroment.py```:
2.1 Set the correct SITE_URL
3. Consider migrating the database to a production-grade database such as [PostgreSQL](https://www.postgresql.org/) and editing ```DATABASES``` in ```tau_factor/tau_factor/settings.py```.
4. You also probably want to configure [Gunicorn WSGI server](https://gunicorn.org/) and [Nginx](https://www.nginx.com/) Gateway.

## Administrator Access

If you wish to manage data of your site, you can use the admin portal at
```http://${SITE_URL}/admin/```.
In order to create a superuser run the following command:
```sh
cd tau_factor
python manage.py createsuperuser
```

## API Documentation

You can access the API documentation at ```http://${SITE_URL}/redoc/``` or ```http://${SITE_URL}/swagger/```.

## Testing

There are currently no tests for this project.

## License

MIT
