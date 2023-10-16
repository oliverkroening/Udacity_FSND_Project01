# Full Stack API Final Project


## Project Description

TriviaAPI is a web application to hold a simple trivia to test the general knowledge of users.
The web application contains a frontend and a backend. The backend provides API endpoints to interact directly with the PostgreSQL database.
Therefor, the web application provides the following functions:

1. Display questions - both all questions and by category can be displayed. Questions should show the question, category and difficulty rating by default and can show/hide the answer.
2. Delete questions - the user can delete questions from the database.
3. Add questions and require that they include question and answer text - the user can create new questions.
4. Search for questions based on a text query string.
5. Play the quiz game, randomizing either all questions or within a specific category.

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

```GET '/api/v1.0/categories'``` 

#### GET Requests

##### GET '/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Input arguments: 
  - ```None```
- Output:
  - ```'success'``` (boolean: information whether the request was successful)
  - ```'categories'``` (dictionary: available categories in database)
- Example: 
  - ```curl http://127.0.0.1:5000/categories``` 
- Returns:
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
- Error handling: 
  - ```HTTP status code 404 NOT FOUND``` in case no categories available

##### GET '/questions?page=${integer}'
- Fetches a paginated set of questions, a total number of questions, all categories and current category string.
- the number of paginated questions is set to 10
- Input: 
  - ```None```
- Output:
  - ```'success'``` (boolean: information whether the request was successful)
  - ```'questions'``` (dictionary: paginated questions in database)
  - ```'total_questions'``` (integer: number of total questions in database)
  - ```'categories'``` (dictionary: available categories in database)
- Example: 
  -```curl http://127.0.0.1:5000/questions```
- Returns:
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
- Error handling: 
  - ```HTTP status code 404 NOT FOUND``` in case no categories available
  - ```HTTP status code 404 NOT FOUND``` in case no questions available

##### GET '/categories/${int:id}/questions'
- Fetches questions for a category specified by id request argument 
- Input: 
  - ```id``` (integer: id of category)  
- Output:
  - ```'success'``` (boolean: information whether the request was successful)
  - ```'questions'``` (dictionary: paginated questions that belong to category)
  - ```'total_questions'``` (integer: number of related questions)
  - ```'current_category'``` (string: name of selected category)
- Example: 
  - ```curl http://127.0.0.1:5000/categories/1/questions```
- Returns:
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
- Error handling: 
  - ```HTTP status code 404 NOT FOUND``` in case requested category not found
  - ```HTTP status code 500 INTERNAL SERVER ERROR``` in case filtering failed due to server error

### DELETE Requests

##### DELETE '/questions/${int:id}'
- Deletes a specified question using the id of the question
- Input: 
  - ```id``` (integer: ID of question to delete)
- Output:
  - ```'success'``` (boolean: information whether the request was successful)
  - ```'deleted_question'``` (integer: ID of deleted question)
- Example: 
  - ```curl -X DELETE http://127.0.0.1:5000/questions/5```
- Returns:
```
{
  "deleted_question": 5,
  "success": true
}
```
- Error handling: 
  - ```HTTP status code 404 NOT FOUND``` in case requested question not found
  - ```HTTP status code 422 UNPROCESSABLE``` in case deletion is not processable

### POST Requests

##### POST '/quizzes'
- Sends a post request in order to get the next question. The question is chosen randomly from a specific category and does not match previous questions.
- Input:
  - ```'previous_questions'``` (list: question id's as integer values)
  - ```'quiz_category'``` (dictionary: chosen category for the quiz)
  - input data from POST request in the following JSON format:
  ```{
    "previous_questions": [1,2,3],
    "quiz_category": {"type": "Science", "id": "1"}
  }``` 
Output:
  - ```'success'``` (boolean: information whether the request was successful)
  - ```'question'``` (dictionary: formatted random question from database)
  - ```'message'``` (string: output in case there are no unused questions left)
- Example: 
  - ```curl -X POST -H "Content-Type: application/json" -d '{"previous_questions": [1, 2, 3], "quiz_category": {"type": "Science", "id": "1"}}' http://127.0.0.1:5000/quizzes```
- Returns:
```
{
    "question": {
        "answer": "The Liver",
        "category": 1,
        "difficulty": 4,
        "id": 20,
        "question": "What is the heaviest organ in the human body?"
    },
    "success": true
}
```
- Error handling: 
  - ```HTTP status code 422 UNPROCESSABLE``` in case filtering is not processable

##### POST '/questions'
- Sends a post request in order to add a new question
- Input: 
  - input data from POST request in the following JSON format:
  ```{
    "question": "This is a question?",
    "answer": "this is an answer", 
    "category": 1, 
    "difficulty": 5, 
  }```
- Output:
  - ```'success'``` (boolean: information whether the request was successful)
  - ```'created_question'``` (integer: ID of created question)
  - ```'questions'``` (dictionary: paginated questions in database)
  - ```'total_questions'``` (integer: number of total questions)
- Example: 
  - ```curl -X POST - H "Content-Type: application/json" -d '{"question": "This is a question?", "answer": "this is an answer", "difficulty": 1, "category": "5"}' http://127.0.0.1:5000/questions```
- Returns: 
```
{
  "success": true
  "created_question": 24
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
  "total_questions": 24
}
```
- Error handling: 
  - ```HTTP status code 422 UNPROCESSABLE``` in case any field for the new question is None
  - ```HTTP status code 422 UNPROCESSABLE``` in case request for creation of new questions is unprocessable

##### POST '/questions/search'
- Sends a post request in order to search for a specific question by search term
- Input:
  - input data from POST request in the following JSON format:
  ```{"searchTerm": "title"}```
- Output:
  - ```'success'``` (boolean: information whether the request was successful)
  - ```'questions'``` (dictionary: paginated questions that include search term)
  - ```'total_questions'``` (integer: number of found questions)
Example: 
  - ```curl -X POST -H "Content-Type: application/json" -d '{"searchTerm": "title"}' http://127.0.0.1:5000/questions/search```
- Returns: 
```
{
    "questions": [
        {
            "answer": "Edward Scissorhands",
            "category": 5,
            "difficulty": 3,
            "id": 6,
            "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
        }
    ],
    "success": true,
    "total_questions": 1
}
```
- Error handling: 
  - ```HTTP status code 404 NOT FOUND``` in case search term does not match any questions
  

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
