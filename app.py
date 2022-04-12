from api import create_app
from flask import url_for

# ========================================================
# Run App
# ========================================================
app = create_app('testing')


def runserver():
    print("Server is runing")
    app.run(host='0.0.0.0', port=5050)


if __name__ == '__main__':
        runserver()


