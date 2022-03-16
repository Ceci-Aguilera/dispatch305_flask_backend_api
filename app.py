from api import create_app

# ========================================================
# Run App
# ========================================================
app = create_app('production')


def runserver():
    print("Server is runing")
    app.run(port=5050)


if __name__ == '__main__':
        runserver()