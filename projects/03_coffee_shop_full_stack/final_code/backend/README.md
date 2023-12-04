# Coffee Shop Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Environment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virtual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) and [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) are libraries to handle the lightweight sqlite database. Since we want you to focus on auth, we handle the heavy lift for you in `./src/database/models.py`. We recommend skimming this code first so you know how to interface with the Drink model.

- [jose](https://python-jose.readthedocs.io/en/latest/) JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTS.

## Running the server

From within the `./src` directory first ensure you are working using your created virtual environment.

Each time you open a new terminal session, run:

```bash
export FLASK_APP=api.py;
```

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## Tasks

### Setup Auth0

1. Create a new Auth0 Account ** DONE **
2. Select a unique tenant domain ** DONE **
	- tenant name: dev-j3q44hh5n3sv0ndq
3. Create a new, single page web application **DONE **
	- application name: Coffee Shop
	- domain: dev-j3q44hh5n3sv0ndq.us.auth0.com
	- client ID: yxA43g9TW1PqJs8cUueqIQtDyjUpYaU5
	- Application Login URI: https://127.0.0.1:8080/login
	- Allowed Callback URLs: https://127.0.0.1:8080/login-results
	- Allowed Logout URLs: https://127.0.0.1:8080/logout
4. Create a new API ** DONE **
	- API name: Coffee
	- API identifier: coffee
	- Signing Algorithm: RS256
   - in API Settings:
     - Enable RBAC ** DONE **
     - Enable Add Permissions in the Access Token ** DONE **
5. Create new API permissions: ** DONE **
   - `get:drinks`
   - `get:drinks-detail`
   - `post:drinks`
   - `patch:drinks`
   - `delete:drinks`
6. Create new roles for: ** DONE **
   - Barista
     - can `get:drinks-detail`
   - Manager
     - can perform all actions
7. Test your endpoints with [Postman](https://getpostman.com).
   - Register 2 users - assign the Barista role to one and Manager role to the other. ** DONE **
   - Sign into each account and make note of the JWT.
   - Import the postman collection ** DONE **`./starter_code/backend/udacity-fsnd-udaspicelatte.postman_collection.json`
   - Right-clicking the collection folder for barista and manager, navigate to the authorization tab, and including the JWT in the token field (you should have noted these JWTs). ** DONE **
   - Run the collection and correct any errors. ** DONE **
   - Export the collection overwriting the one we've included so that we have your proper JWTs during review! ** DONE **

### Implement The Server

There are `@TODO` comments throughout the `./backend/src`. We recommend tackling the files in order and from top to bottom:

1. `./src/auth/auth.py`
2. `./src/api.py`
