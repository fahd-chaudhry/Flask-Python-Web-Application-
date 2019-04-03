# Flask-Python-Web-Application
Python-Flask web application with RESTful API using mySQL database. 
Provisioned using Vagrant into a Virtual Box VM.

## To test this website please follow these steps:

1. Clone branch/pull to latest release.<p>
2. Enter the following commands in terminal in the given order: 
  - `Vagrant up` <p>
  - `vagrant provision` (if you have pulled the code before) <p>
  - `vagrant ssh` <p>
  - `cd /project` <p>
  - `sudo python techDemoApp.py` <p>
    
3. Enter the URL `localhost:5000` into any browser on your local machine to view the web application. <p>

### Functionality Implemented: <p>
1. User registration and login/logout functionality. <p>
2. Ability to create/edit/delete articles. <p>
3. View articles written by all users once a user has logged in. <p>
4. Dashboard displays only the logged in user's articles. <p>
5. Articles and Users are saved in a mySQL database. <p>

### Please note: If you get a vagrant port error, please open the vagrant file and change the host port for the SQL server to a unique value. <p>

### Contact information <p>
fahd.chaudhry@yahoo.com
