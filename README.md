# DISPATCH305 FLASK BACKEND API


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


1. Create virtualenv and Pip install dependencies:
    ```
        pip install -r requirements.txt
    ```

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
    ```
	or
    2. Copy the the content of the .example.env file to the .env file:
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













<a name="useful_links"></a>
### Useful Links

#### Database (PostgreSQL and SQLAlchemy)

- Set up postgreSQL in Ubuntu (install + create database, user, and alter roles): [Link from DigitalOcean about deploying Django + Postgresql](https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-16-04)
- Create models and connecting them to the db using SQLAlchemy: [Link to Flask-SQLAlchemy official documentation](https://flask-sqlalchemy.palletsprojects.com/en/2.x/)
- Managing Foreing Keys: One to One, One to Many, and Many to One: [Link to Flask-SQLAlcgemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/models/)


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
- [Pyhton Slim Buster error with gcc](https://github.com/watson-developer-cloud/python-sdk/issues/418)
- Using sh file in docker to init flask and run migrations: [Fix slim-buster with netcat, gcc, and g++](https://stackoverflow.com/questions/61726605/docker-entrypoint-sh-not-found)
- Why not using volumes in docker-compose for flask files: [Fix migrations folder is created and not empty error](https://stackoverflow.com/questions/69297600/why-isnt-my-dockerignore-file-ignoring-files)













