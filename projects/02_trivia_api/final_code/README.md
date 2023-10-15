# Full Stack API Final Project


## Project Description

Udacity is invested in creating bonding experiences for its employees and students. A bunch of team members got the idea to hold trivia on a regular basis and created a webpage to manage the trivia app and play the game, but their API experience is limited and still needs to be built out.

That's where you come in! Help them finish the trivia app so they can start holding trivia and seeing who's the most knowledgeable of the bunch. The application must:

1. Display questions - both all questions and by category. Questions should show the question, category and difficulty rating by default and can show/hide the answer.
2. Delete questions.
3. Add questions and require that they include question and answer text.
4. Search for questions based on a text query string.
5. Play the quiz game, randomizing either all questions or within a specific category.

Completing this trivia app will give you the ability to structure plan, implement, and test an API - skills essential for enabling your future applications to communicate with others.

## Getting Started

### Installing Dependencies

#### Backend

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)


2. **Virtual Enviornment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)


3. **PIP Dependencies** - Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:
```bash
pip install -r requirements.txt
```
This will install all of the required packages we selected within the `requirements.txt` file.


4. **Key Dependencies**
 - [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

 - [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

 - [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

#### Frontend

1. **Installing Node and NPM**<br>
This project depends on Nodejs and Node Package Manager (NPM). Before continuing, you must download and install Node (the download includes NPM) from [https://nodejs.com/en/download](https://nodejs.org/en/download/).

2. **Installing project dependencies**<br>
This project uses NPM to manage software dependencies. NPM Relies on the package.json file located in the `frontend` directory of this repository. After cloning, open your terminal and run:
```bash
npm install
```
>_tip_: **npm i** is shorthand for **npm install**

### Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

### Running the backend server

From within the `./src` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.


### Running Your Frontend in Dev Mode

The frontend app was built using create-react-app. In order to run the app in development mode use ```npm start```. You can change the script in the ```package.json``` file. 

Open [http://localhost:3000](http://localhost:3000) to view it in the browser. The page will reload if you make edits.<br>

```bash
npm start
```

## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```

## API documentation

### Getting Started
- Backend Base URL: [http://127.0.0.1:5000/](http://127.0.0.1:5000/)
- Frontend Base URL: [http://127.0.0.1:3000/](http://127.0.0.1:3000/)

### Endpoints

GET '/api/v1.0/categories'

#### GET Requests

##### GET '/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains an object of id: category_string key:value pairs.
- Example: ```curl http://127.0.0.1:5000/categories``` 
```
{
    'categories': {
	'1' : "Science",
    	'2' : "Art",
    	'3' : "Geography",
    	'4' : "History",
    	'5' : "Entertainment",
    	'6' : "Sports" 
	},
	'success': True
}
```

##### GET '/questions?page=${integer}'
- Fetches a paginated set of questions, a total number of questions, all categories and current category string. 
- Request Arguments: page - integer
- Returns: An object with 10 paginated questions, total questions, object including all categories, and current category string
- Example: ```curl http://127.0.0.1:5000/questions```
```
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "questions": [
    {
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
    {
      "answer": "Muhammad Ali",
      "category": 4,
      "difficulty": 1,
      "id": 9,
      "question": "What boxer's original name is Cassius Clay?"
    },
    {
      "answer": "Apollo 13",
      "category": 5,
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    },
    {
      "answer": "Tom Cruise",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    },
    {
      "answer": "Edward Scissorhands",
      "category": 5,
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    },
    {
      "answer": "Brazil",
      "category": 6,
      "difficulty": 3,
      "id": 10,
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    },
    {
      "answer": "Uruguay",
      "category": 6,
      "difficulty": 4,
      "id": 11,
      "question": "Which country won the first ever soccer World Cup in 1930?"
    },
    {
      "answer": "George Washington Carver",
      "category": 4,
      "difficulty": 2,
      "id": 12,
      "question": "Who invented Peanut Butter?"
    },
    {
      "answer": "Lake Victoria",
      "category": 3,
      "difficulty": 2,
      "id": 13,
      "question": "What is the largest lake in Africa?"
    },
    {
      "answer": "The Palace of Versailles",
      "category": 3,
      "difficulty": 3,
      "id": 14,
      "question": "In which royal palace would you find the Hall of Mirrors?"
    }
  ],
  "success": true,
  "total_questions": 23
}
```

##### GET '/categories/${int:id}/questions'
- Fetches questions for a category specified by id request argument 
- Request Arguments: id - integer
- Returns: An object with questions for the specified category, total questions, and current category string
- Example: ```curl http://127.0.0.1:5000/categories/1/question```
``` 
{
  "current_category": "Science",
  "questions": [
    {
      "answer": "The Liver",
      "category": 1,
      "difficulty": 4,
      "id": 20,
      "question": "What is the heaviest organ in the human body?"
    },
    {
      "answer": "Alexander Fleming",
      "category": 1,
      "difficulty": 3,
      "id": 21,
      "question": "Who discovered penicillin?"
    },
    {
      "answer": "Blood",
      "category": 1,
      "difficulty": 4,
      "id": 22,
      "question": "Hematology is a branch of medicine involving the study of what?"
    }
  ],
  "success": true,
  "total_questions": 3
}
```

### DELETE Requests

##### DELETE '/questions/${id}'
- Deletes a specified question using the id of the question
- Request Arguments: ```id``` - integer
- Returns: Does not need to return anything besides the appropriate HTTP status code.
- Example: ```curl -X DELETE http://127.0.0.1:5000/questions/5```
```
{
  "deleted_question": 5,
  "success": true
}
```

### POST Requests

##### POST '/quizzes'
- Sends a post request in order to get the next question 
- Request Body: 
{```'previous_questions'```:  an array of question id's such as ```[1, 4, 20, 15]```
```'quiz_category'```: a string of the current category }
- Returns: a single new question object 
- Example: ```curl -X POST -H "Content-Type: application/json" -d '{"previous_questions": [2, 6], "quiz_category": {"type": "Entertainment", "id": "5"}}' http://127.0.0.1:5000/quizzes```
```
{
	"question": {
		"answer": "Tom Cruise",
		"category": 5,
		"difficulty": 4,
		"id": 4,
		"question": "What actor did author Anne Rice first 		denounce, then praise in the role of her beloved 			Lestat?"
  	}, 
  	"success": true
}
```

##### POST '/questions'
- Sends a post request in order to add a new question
- Example: ```curl -X POST - H "Content-Type: application/json" -d '{"question": "Who is Donald Trump?", "answer": "the current president of US", "difficulty": 1, "category": "5"}' http://127.0.0.1:5000/questions```
- Returns: Does not return any new data
```
{
  "success": true
  "created": 19
  "total_questions": 19
}
```

##### POST '/questions/search'
- Sends a post request in order to search for a specific question by search term
- Returns: any array of questions, a number of totalQuestions that met the search term and the current category string 
Example: ```curl -X POST -H "Content-Type: application/json" -d '{"searchTerm": "peanut butter"}' http://127.0.0.1:5000/questions/search```
```
{
  "questions": [
    {
      "answer": "George Washington Carver", 
      "category": 4, 
      "difficulty": 2, 
      "id": 12, 
      "question": "Who invented Peanut Butter?"
    }
  ], 
  "success": true, 
  "total_questions": 1
}
```

### Error Handling
Errors are returned in the following JSON format:
```
{
    'success': False,
    'error': 404,
    'message': 'Resource not found'
}
```

The API returns 4 types of error:
- 400: Bad request
- 404: Not found
- 422: Unprocessable Entity
- 500: Internal Server Error

## Author and Acknowledgement
Oliver Kröning contributed to following files within this project:
- API (```/backend/flaskr/__init.py__```)
- test file (```/backend/test_flaskr.py```)
- this documentation (```README.md```)

The project and other files are credited to [Udacity](https://www.udacity.com/).
