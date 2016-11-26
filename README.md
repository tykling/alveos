# alveos
An IRC webchat for the baconsvin network. Based on django, django-channels, irc3.

## Requirements
Alveos requires Python3 because irc3 uses asyncio which is irc3 only these days. The rest of the requirements are listed in requirements.txt.

## Setup dev environment
* virtualenv -p python3 venv
* source venv/bin/activate
* pip install -r requirements.txt
* python manage.py migrate
* python manage.py runserver

