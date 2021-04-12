# 💰 Splitwise API

Create group with your friends and split bills without any hassle.

## Demo 🖥️

You can test the live API [here](https://documenter.getpostman.com/view/4935333/TzJoDzxS).

## Features ⭐

⚡️ Add users/members to the application (CURD)\
⚡️ Create groups and add new members to the group (CRUD)\
⚡️ Add expenses in the group and let the application handle all the spliting

## Folder Structure :file_folder:

```
.
├── Procfile
├── app.py
├── application
│   ├── __init__.py
│   ├── config
│   │   └── __init__.py
│   ├── controllers
│   │   ├── expense.py
│   │   ├── group.py
│   │   └── user.py
│   └── models
│       ├── expense.py
│       ├── group.py
│       ├── transaction.py
│       ├── user.py
│       └── user_group.py
├── practice.py
├── requirements.txt
├── runtime.txt
└── wsgi.py
```

Entry point is `app.py`. All the models are being stored in `models`. All the routes are structured in `controllers`.

## Install & Build 🛠️

**Step 1:** Install all the dependencies.

```
pip install -r requirements.txt
```

**Step 2:** Run the server. (Make sure `.env` is already has all the required environment variables)

```
python app.py
```

## Deployment 📦

This is a [Flask](https://flask.palletsprojects.com/en/1.1.x/) backend application hosted on [Heroku](https://heroku.com/).

The `wsgi.py` contains the direct run code for the application. It is being executed by `gunicorn` in `Procfile`. Heroku directly executes `Procfile` and starts the server.

This API has also been documented at [Postman](https://www.postman.com/). You can test it [here](https://documenter.getpostman.com/view/4935333/TzJoDzxS).
