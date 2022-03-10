# DISPATCH305 FLASK BACKEND API

### Intallation

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