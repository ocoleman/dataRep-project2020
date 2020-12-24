# dataRep-project2020
Project Assessment for Data Representation in 2020

http://owenproj2020.pythonanywhere.com/
<br>

## How to run

Firstly, clone this repository to your local machine. From there use a command terminal to cd into the newly created directory. It is recommended you use a virtual environment when interacting with this project. Do so with the follow commands "python -m venv venv" and then ".\venv\Scripts\activate.bat" (to deactive type "deactivate"). 

NOTE: Ensure you have the python virtualenv package before attempting to create a virtual environment.

Next, enter the following command to install flask and the other packages required by this application: "pip install -r requirements.txt". Finally, set the FLASK_APP environment variable equal to server.py as follows "set FLASK_APP=server.py". You should now be able to run the application by simply typing "flask run".
<br>

## database.sql
Below is the sql I used when creating the database tables for this project.
```sql
use datarepresentation;

create table user ( id int NOT NULL AUTO_INCREMENT,
username varchar(250),
password varchar(250),
PRIMARY KEY(id));

create table questions ( id int NOT NULL AUTO_INCREMENT, 
author varchar(250), 
category varchar(250), 
correct_answer varchar(250), 
incorrect_answers varchar(250),
type varchar(250),
difficulty varchar(250),
question varchar(250),
PRIMARY KEY(id));
```

## Sources 
List of sources used during this project.
1. Flask Documentation, Quickstart , https://flask.palletsprojects.com/en/1.1.x/quickstart/
2. Bootstrap, https://getbootstrap.com/
3. pythonanywhere, Setting up Flask applications on PythonAnywhere, https://help.pythonanywhere.com/pages/Flask/
4. Open Trivia DB, Trivia API, https://opentdb.com/api_config.php
