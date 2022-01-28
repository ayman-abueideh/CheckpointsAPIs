# CheckPoint Task

## Facts

* Checkpoint has a static location
* Traveller has the option to claim checkpoint’s current state
* Trusted traveller’s claim has bigger effect on checkpoint’s state
* Traverller’s calim invalidates by time
* Traveller shall not claim a checkpoint state more than once within a period of time
* Minimum number of claims is required to determine checkpoint’s state
* Travellers can subscribe to be notified once a checkpoint is closed

## APIs

* Get all the subscriber subscribed checkpoints now .
* Add an api to claim a checkpoint state .
* Add an api to get the trusted level of a user:-
    * Trusted level is the number of wrong claims / number of claims 




### Prerequisites
* Python 3.8

### Setting up the server 
* Clone the repo
* create virtual environment 
* install the requirements: `pip install -r requirements.txt` 
* migrate the models: `python manage.py migrate`
* run the server: `python manage.py runserver`
