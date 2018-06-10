# demo-blog
A demonstration blog as a simple example of some technologies that I intergrate into the django framework

## Requirements
The code will run in the supplied vagrant instance but if you wanted to run the webserver outside of this you would require
* Django==2.0.5
* pytz==2018.4
* Pillow==4.3.0

## Setup
To initially setup an instance using the vagrant, go to the root directory and run the command `vagrant up` this will start a vagrant instance. Once available ssh into the vagrant instance and run `python3 manage.py migrate` in the vagrant directory to build a database. following that run `python3 manage.py createsuperuser` to create your first super user. When this is all completed to start the webserver by running `python3 manage.py runserver 0.0.0.0:8080` and the website will be accessible from 127.0.0.1:8080
