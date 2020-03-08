# Simple Event API
Create and manipulate events and sessions. Events can have multiple sessions.

## Installation and running
Two possibilities to run the service have been implemented:

### Docker
The preferred method to run the service is through the docker. This means that the machine, on which the the service is running, only needs a docker instance running, with no specific Python dependencies. To build the image, run:
```
docker-compose build
```
and to run it in the background, run:
```
docker-compose up
```
which will run the service on the host `0.0.0.0` under the port `8000`. To verify it's running, access e.g. docs at `http://0.0.0.0:8000/`.


### Direct Python call
To run the service natively on the host machine, one needs to manage the virtualenv, install requirements:
```
pip install -r requirements.txt
```

The service itself can be ran through the `manage.py` script:
```
python manage.py runserver
```
This is a testing server, which is being reloaded on each change in the underlying python files. To access the documentation, please access standard Django Rest Framework docs at `http://127.0.0.1:8000/`.


## Development
### Testing
To run the tests, install testing dependencies:
```
pip install -r requirements-dev.txt
```
and run the tests through `pytest`, e.g.:
```
DJANGO_SETTINGS_MODULE=event.settings pytest -sxk "" eventplanner/tests.py --cov=eventplanner --cov-report=term-missing
```
which, besides running all tests, will also return the coverage report:
```
----------- coverage: platform linux, python 3.7.6-final-0 -----------
Name                                      Stmts   Miss  Cover   Missing
-----------------------------------------------------------------------
eventplanner/__init__.py                      0      0   100%
eventplanner/admin.py                         1      0   100%
eventplanner/migrations/0001_initial.py       7      0   100%
eventplanner/migrations/__init__.py           0      0   100%
eventplanner/models.py                       19      0   100%
eventplanner/serializers.py                  27      0   100%
eventplanner/urls.py                          8      0   100%
eventplanner/views.py                        18      0   100%
-----------------------------------------------------------------------
TOTAL                                        80      0   100%
```

The code is compliant with basic `flake8` linting and has been formatted with `black` allowing for the 120 characters in a line, which is a personal favourite of mine.
