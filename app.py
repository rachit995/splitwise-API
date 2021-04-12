# coding: utf-8
from application import create_app
# Used by app debug & livereload
PORT = 5000
app = create_app()


def run():
    """Run app."""
    app.run(port=PORT, debug=True, host='0.0.0.0')


if __name__ == "__main__":
    run()
