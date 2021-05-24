# Coffee Shop Full Stack

Udacity has decided to open a new digitally enabled cafe for students to order drinks, socialize, and study hard. The coffee shop app enables baristas to see recipes information and managers to create and update drinks.

## Application Stack

Flask, SQLite and SQLAlchemy backend with Ionic frontend. Auth0 is used for authentication and authorization.

## Get Started

### Backend

Configure a virtual environment. Follow this [link](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/) for instructions.

From the `/backend` directory:

#### Install dependencies

```
pip install -r requirements.txt
```

From the `/backend/src` directory:

#### Run server

```
export FLASK_APP=api.py;
```

```
flask run --reload
```

### Frontend

From the `/frontend` directory:

```
npm install
```

#### Run Ionic server

If you don't have the Ionic CLI installed on your machine run:

```
npm install -g @ionic/cli
```

```
ionic serve
```