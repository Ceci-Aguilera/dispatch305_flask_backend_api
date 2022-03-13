# DISPATCH305 FLASK BACKEND API


# Table of Contents
1. [Installation](#installation)
4. [Useful Links](#useful_links)




<a name="installation"></a>
### Installation

1. Clone Repo
    ```
        git clone https://github.com/Ceci-Aguilera/dispatch305_flask_backend_api.git
    ```


1. Create virtualenv and Pip install dependencies:
    ```
        pip install -r requirements.txt
    ```

1. Set up postgresql database. For development the default credentials are:
    ```
        Database name: test_db
        Database user: test_user
        Database password: test_pass
        Database host: localhost
        Database port: 5432
    ```
1. Create .env file inside config folder and set up the following env variables:
	```
    	SECRET_KEY (for example "someSecretKey")
        JWT_SECRET_KEY (use secrets.token_hex(16) from python secrets)
        SECURITY_PASSWORD_SALT (for example "someSecurityPassword")
        ADMIN_EMAIL_CREDIENTIAL (email to use to create a Admin user)
        ADMIN_PASSWORD_CREDENTIAL (the password for the Admin user)
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

1. Congratulations =) !!! the app should be running in [localhost:5000](http://localhost:5000)





<a name="useful_links"></a>
### Useful Links

#### Database (PostgreSQL and SQLAlchemy)

- Set up postgreSQL in Ubuntu (install + create database, user, and alter roles): [Link from DigitalOcean about deploying Django + Postgresql](https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-16-04)
- Create models and connecting them to the db using SQLAlchemy: [Link to Flask-SQLAlchemy official documentation](https://flask-sqlalchemy.palletsprojects.com/en/2.x/)

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
	- [Link to Custom Formatter Stackoverflow implementation for url field](https://stackoverflow.com/questions/37258668/flask-admin-how-to-change-formatting-of-columns-get-urls-to-display)
















