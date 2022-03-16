)# DISPATCH305 FLASK BACKEND API


# Table of Contents
1. [Quick Installation for testing using Docker](#docker)
2. [Custom Installation](#installation)
3. [Structure and apps](#structure)
4. [Deploying in VPS](#deploy)
5. [Connecting to the React frontend](#frontend)
6. [Screenshots of the Admin Panel](#screenshots)
7. [Screenshots of the Frontend React App](#screenshots_frontend)
8. [Useful Links](#useful_links)







<a name="docker"></a>
### Quick Installation for testing using Docker

1. Clone Repo
    ```
        git clone https://github.com/Ceci-Aguilera/dispatch305_flask_backend_api.git
    ```
1. Install Docker and Docker Compose
1. Config the env variables using one of the following methods:
	1. Create .env file inside the config folder and set up the following env variables:
	```
    	SECRET_KEY                 		(for example "someSecurityPassword")
        JWT_SECRET_KEY                  (use secrets.token_hex(12) from python secrets)
        SECURITY_PASSWORD_SALT          (for example "someSecurityPassword")
        ADMIN_EMAIL_CREDIENTIAL         (email to use to create a Admin user)
        ADMIN_PASSWORD_CREDENTIAL       (the password for the Admin user)
        MAIL_SERVER						(the server for sending emails using Flask-Mail)
        MAIL_PORT
        MAIL_PASSWORD
        MAIL_STRING_ID					(a short random string to pass when using office 365)
    ```
	or
    2. Copy and modify the content of the .example.env file to the .env file:
    ```
    	cp config/.example.env config/.env
    ```

1. Run the command:
   ```
       docker-compose up -d --build
   ```
1. Congratulations =) !!! the app should be running in [localhost:5000](http://localhost:5000)




















<a name="installation"></a>
### Custom Installation

1. Clone Repo
    ```
        git clone https://github.com/Ceci-Aguilera/dispatch305_flask_backend_api.git
    ```


1. Create a virtual env and Pip install dependencies:
    ```
        pip install -r requirements.txt
    ```

1. Open the app.py file and change the parameter of create_app to 'development' (by default it is set to production)

1. Set up postgresql database ([See Useful Links](#useful_links)). For development the default credentials are:
    ```
        Database name: test_db
        Database user: test_user
        Database password: test_pass
        Database host: localhost
        Database port: 5432
    ```
1. Config the env variables using one of the following methods:
	1. Create .env file inside the config folder and set up the following env variables:
	```
    	SECRET_KEY                 		(for example "someSecurityPassword")
        JWT_SECRET_KEY                  (use secrets.token_hex(12) from python secrets)
        SECURITY_PASSWORD_SALT          (for example "someSecurityPassword")
        ADMIN_EMAIL_CREDIENTIAL         (email to use to create a Admin user)
        ADMIN_PASSWORD_CREDENTIAL       (the password for the Admin user)
        MAIL_SERVER						(the server for sending emails using Flask-Mail)
        MAIL_PORT
        MAIL_PASSWORD
        MAIL_STRING_ID					(a short reandom string to pass when using office 365)
    ```
	or
    2. Copy and modify the content of the .example.env file to the .env file:
    ```
    	cp config/.example.env config/.env
    ```

1. Run the migrations
    ```
        flask db init
        flask db migrate
        flask db upgrade
    ```

    __NOTE:__ In case of an error regarding revision of migration, run:
    ```
        flask db revision --rev-id <revision_id_in_error>
        flask db migrate
        flask db upgrade
    ```

1. Run the app
    ```
        flask run
    ```

    or
    ```
    	python app.py
    ```

__NOTE:__ The command __flask run__ will run the app with the default config from flask (debug=False, ...) while __python app.py__ will run the app with the custom config set in the file  __config/config.py__. To change the initial configuration edit the files __app.py__ and __config/config.py__ files. The env variables for the __config/config.py__ files are retrieved from __config/.env__ using __decouple.config__.

1. Congratulations =) !!! the app should be running in [localhost:5000](http://localhost:5000) for _flask run_ or [localhost:5050](http://localhost:5050) if using _python app.py_.












<a name="structure"></a>
### Structure and Apps

#### Brief Introduction
Dipatch305 is a service that helps dispatchers communicates with both divers and brokers. From now on, we call DISPATCH305 to refer to the company, and also  _drivers_ will be called _clients_ while _dispatchers_ will be called _staff members_. In addition, the services offered by the website will be referred as:
- _Searching a Cargo_: When a client requests the dispatcher to look out for an Agency with a Cargo to transport from a point in the map to another. In this case the staff member should contact a broker (Agency) and make the arraignments.
- _Sending Analytics_: Every Friday, a bill should be sent to every client with the weekly pending bill amount, and a description of the charges. In addition, for the clients with a VIP account, an analytics resume of the week should also be sent.
- _Managing POD_: When a Cargo is delivered, the VIP clients may request the staff member to manage the sending of the _Rate Conf_ and the _POD_ (this are 2 PDF files needed as proof of service and delivery).

#### Basic Workflow of the Website
1. First, the client registers at [dispatch305.com](https://www.dispatch305.com/create-account) (the Frontend website created using REACT.js). During this step, the client should provide basic account information such as name, company, ..., and should also upload the 4 basic PDF files that most brokers require for hiring them to deliver cargo.
2. When the new account is created, it is set to inactive and the _Admin User_ is notified. The, the _Admin User_ assigns a staff member to the client. From this point on, the staff member is said to be the client's dispatcher. The client must download the PDF that is under the section Agreement in the Frontend app. Once this steps are completed, the client's account is set to active.
3. From now on, clients with a plan BASICO (basic account) can request the dispatcher to offer the service of _Searching a Cargo_, while VIP clients can ask for the services of _Searching a Cargo_, _Sending Analytics_, and  _Managing POD_. Regardless of which type of account a client has, a Bill will be sent to them with the pending amount to pay for the services offered in that week from DISPATCH305. When a user fails to pay the weekly bill (usually a timeline of 3 days offered), the account becomes inactive until the bill is paid.
4. After the user requests a _Searching a Cargo_ service, and the Cargo is found by the staff member, and later delivered by the client, if the client has a VIP account, the staff member can be requested to offer a _Managing POD_ service. In order to do that, the client must send the PDF files required, and the staff member should upload them to DISPATCH305's Admin Panel.











<a name="deploy"></a>
### Deploy to VPS using PostgreSQL, Nginx, and Gunicorn

1. Clone the repo:
```
	git clone https://github.com/Ceci-Aguilera/dispatch305_flask_backend_api.git
```
2. Install the dependencies:
```
	sudo apt-get update
	sudo apt-get install python3-pip python3-dev libpq-dev postgresql postgresql-contrib nginx
```
3. Set up postgresql database ([See Useful Links](#useful_links))
4. Create .env file and configure the env variables
5. Create a virtual env and activate it:
```
	virtualenv myprojectenv
    source myprojectenv/bin/activate
```
6. Pip install the requirements:
```
	pip install -r requirements.txt
```
7. Pip install gunicorn
```
	pip install gunicorn
```
8. Open app.py and add host='0.0.0.0' to the create_app() function:
9. Test configuration so far:
```
	flask db init
	flask db migrate
    flask db upgrade

    python app.py
```
This could need to delete the migrations folder and create it again (or make revision on migration)
10. Create wsgi.py file:
```
	sudo vim wsgi.py
```
and copy and paste this:
```
  from app import app

  if __name__ == "__main__":
      app.run()

```
and then
```
	gunicorn --bind 0.0.0.0:5050 wsgi:app
```

11. Complete the setup of the website with this [link](https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-gunicorn-and-nginx-on-ubuntu-20-04)

12. Set up Cors to allow the frontend to fetch and post requests ([See Useful Links](#useful_links))




















<a name="useful_links"></a>
### Useful Links

#### Database (PostgreSQL and SQLAlchemy)

- Set up postgreSQL in Ubuntu (install + create database, user, and alter roles): [Link from DigitalOcean about deploying Django + Postgresql](https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-16-04)
- Create models and connecting them to the db using SQLAlchemy: [Link to Flask-SQLAlchemy official documentation](https://flask-sqlalchemy.palletsprojects.com/en/2.x/)
- Managing Foreign Keys: One to One, One to Many, and Many to One: [Link to Flask-SQLAlcgemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/models/)


#### Authentication and Admin Panel

- Flask with JWT Authentication (For calls coming from the REACT frontend): [Link to Flask-JWT-Extended official documentation](https://flask-jwt-extended.readthedocs.io/en/stable/)
- Flask Security for the Admin Panel (Using Flask-Security-Too instead of Flask Security as it is deprecated): [Link to Flask-Security-Too official documentation](https://flask-security-too.readthedocs.io/en/stable/)
	- Useful Flask-Security-Too links from Github and Stackoverflow:
		- [FS Uniqufiers is mandatory for User model, and get_user function eliminated from version 4.0](https://github.com/Flask-Middleware/flask-security/issues/85)
		- [Custom Login html and overriding other templates](https://stackoverflow.com/questions/47317722/how-do-i-embed-a-flask-security-login-form-on-my-page)
		- [Flask-Security + Flask Admin when Authenticating user Resource 1](https://stackoverflow.com/questions/31091637/how-to-secure-the-flask-admin-panel-with-flask-security)
		- [Flask-Security + Flask Admin when Authenticating user Resource 2](https://gist.github.com/skyuplam/ffb1b5f12d7ad787f6e4)
- Flask Admin Panel:
	- [Link to Flask-Admin official documentation](https://flask-admin.readthedocs.io/en/latest/)
	- [Link to Flask-Admin github](https://github.com/flask-admin/flask-admin)
	- [Link to Custom Formatter in Stackoverflow to implement a custom field](https://stackoverflow.com/questions/37258668/flask-admin-how-to-change-formatting-of-columns-get-urls-to-display)


#### Rest Api using Restx

- [Link to Flask Restx official documentation](https://flask-restx.readthedocs.io/en/latest/)
- [Link to Flask Restx github](https://github.com/python-restx/flask-restx)


#### Managing PDFs and other files
- [Save pdf and other file types from React Frontend](https://medium.com/excited-developers/file-upload-with-react-flask-e115e6f2bf99)
- [Send pdf file to Frontend](https://docs.faculty.ai/user-guide/apis/flask_apis/flask_file_upload_download.html)
- [Render PDF file in Browser using Flask](https://artsysops.com/2021/01/02/how-to-open-a-pdf-file-on-the-browser-with-flask/)


#### Docker and Docker Compose with Flask + Postgresql
- [Dockerize Flask app with Postgresql, Guinicorn and Nginx](https://testdriven.io/blog/dockerizing-flask-with-postgres-gunicorn-and-nginx/#gunicorn)
- [Python Slim Buster error with gcc](https://github.com/watson-developer-cloud/python-sdk/issues/418)
- Using sh file in docker to init flask and run migrations: [Fix slim-buster with netcat, gcc, and g++](https://stackoverflow.com/questions/61726605/docker-entrypoint-sh-not-found)
- Why not using volumes in docker-compose for flask files: [Fix migrations folder is created and not empty error](https://stackoverflow.com/questions/69297600/why-isnt-my-dockerignore-file-ignoring-files)


#### Sending Emails with Flask-Mail:
- [Flask-Mail official documentation](https://pythonhosted.org/Flask-Mail/)
- [Flask-Mail with office 365 services issue with ID Stackoverflow Fix](https://stackoverflow.com/questions/54600601/i-am-using-office-and-flask-mail)

#### Cors Headers Configuration
- [Example of simple Cors config for React js Frontend app](https://stackoverflow.com/questions/64520497/how-would-i-make-it-so-a-flask-api-can-only-be-used-with-my-reactjs-app)
