# alveos
An IRC webchat developed for the baconsvin network. Based on django, django-channels and irc3.


## Requirements
Alveos requires Python3 because irc3 uses asyncio which is python3 only these days. The rest of the requirements are listed in requirements.txt.


## Setup dev environment
* virtualenv -p python3 venv
* source venv/bin/activate
* pip install -r requirements.txt
* python manage.py migrate
* python manage.py runserver


## Data structures used
All messages in Alveos are JSON with the following basic structure:
{
    "alveos_type": "some_type",
    "alveos_version": "alveos_v1",
    "payload": {
        "somekey": "value",
        "otherkey": "foobar"
    }
}

Four message types are defined at the time of writing. They are "from_browser", "alveos_worker_command", "irc3_to_browser", and "alveos_to_browser" and they are documented below.


### 1. Messages from the browser (from_browser)
A user says types something (command or message) in the browser. The message sent from the browser over the websocket has the type "from_browser" and the payload has the following structure:
{"target": "#alveos", "message": "hello world"}
Where target is the name of the window/tab the text was written in, and message is what was written. Stuff triggered by clicking buttons in the client are translated to text commands (beginning with /) before being sent to Django.


### 2. Controlling the IRC worker (alveos_worker_command)
Commands to control the IRC worker have the alveos_type "alveos_worker_command" and the payload has the following structure:
{"command": "die", "reason": "something"}
Where "command" is always present, and the other keys vary (depending on the command).


### 3. IRC messages to the browser (irc3_to_browser)
When something happens on IRC we presently just pass the kwargs irc3 provides in the payload on to the websocket, with the alveos_type "irc3_to_browser". Thus the browser will receive a message with a structure depending on the event (and IRC3). Some examples below:
{"data": None, "event": "JOIN", "channel": "#alveos", "mask": "alveostyk!~irc3@217.71.4.82.static.router4.bolignet.dk"}
{"target": "#alveos", "event": "PRIVMSG", "data": "hej", "mask": "tykling!tykling@example.com"}
This is a temporary solution. The intended design is to make the frontend very lean with all logic inside django. The frontend will basically just receive "print X in window Y" messages over the WS.

### 4. System messages to the browser (alveos_to_browser)
Other messages to the browser are sent with the alveos_type "alveos_to_browser" and a simple payload:
{"message": "Done connecting to IRC server!"}


