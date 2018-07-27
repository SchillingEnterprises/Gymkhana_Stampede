# Beargrass Christian Church
### Youth Tracker
###### Created by <a href="https://schillingenterprises.github.io/Gavin-Schilling-Marketing/">Gavin Schilling Marketing</a>


#### How to run:
Step 1: Installing Python
<br>
<a href="https://www.python.org/downloads/release/latest">Click Here to Install the Latest Version of Python for Your Desired Machine Type</a>

Step 2: Using Pip
```commandline
pip install pip -U
pip install -r requirements.txt
```

Step 3: From Command Line (Starting in project's root directory)
```commandline
python manage.py makemigrations youth
python manage.py migrate youth
```

Step 4: Running on localhost
```commandline
python manage.py runserver
```
##### Run on <a href="http://localhost:8000/">LocalHost 8000</a>


### _**`NOTE: Must be logged in to admin to alter data!`**_