import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

### Global variable definitions
QUESTIONS_PER_PAGE = 10

### Function definitions
def paginate_questions(request, selections):
  '''
  Function to paginate questions of requested selection

  Input: 
    - request (HTTP request to get the arguments)
    - selections (list: questions to paginate)
  
  Output:
    - current_questions (list: paginated questions from selection)
  '''
  page = request.args.get('page', 1, type=int)
  start = (page-1) * QUESTIONS_PER_PAGE
  end = start+QUESTIONS_PER_PAGE 
  questions = [question.format() for question in selections]
  current_questions = questions[start:end]

  return current_questions

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  '''
  @TODO: Set up CORS. Allow '*' for origins. 
  Delete the sample route after completing the TODOs
  ---- Done ----
  '''
  CORS(app, resources={"/": {"origins": "*"}})

  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  ---- Done ----
  '''
  @app.after_request
  def after_request(response):
    '''
    Function to set the HTTP response headers and methods for a response
    after a request to control the access for resources.

    Input: 
      - response (original response for a request)
    
    Output:
      - response (response with modified headers and methods)
    '''
    response.headers.add(
      'Access-Control-Allow-Headers', 'Content-Type, Authorization, true'
    )
    response.headers.add(
      'Access-Control-Allow-Methods', 'GET, PATCH, PUT, POST, DELETE, OPTIONS'
    )
    return response

  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  ---- Done ----
  '''
  @app.route('/categories')
  def get_categories():
    '''
    API endpoint for GET request to get all available categories

    Input: 
      - None
    
    Output:
      - success (boolean: information whether the request was successful)
      - categories (dictionary: available categories in database)
    '''
    # get all categories via database query
    data = Category.query.all()
    # extract all categories and save in dictionary
    categories = {}
    for category in data:
      categories[category.id] = category.type
    
    # create HTTP 404 error (not found) in case there are no categories
    if len(categories) == 0:
      abort(404)

    return jsonify({
      'success': True,
      'categories': categories
    })

  '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the 
  screen for three pages.
  Clicking on the page numbers should update the questions. 
  ---- Done ----
  '''
  @app.route('/questions')
  def get_questions():
    '''
    API endpoint for GET request to get a number of questions (paginated)

    Input: 
      - None
    
    Output:
      - success (boolean: information whether the request was successful)
      - questions (dictionary: paginated questions in database)
      - total_questions (integer: number of total questions)
      - categories (dictionary: available categories in database)
    '''
    # get all questions via database query
    questions = Question.query.all()
    # get total number of questions in database
    total_questions = len(questions)
    # paginate questions
    current_questions = paginate_questions(request, questions)

    # get all categories via database query
    data = Category.query.all()
    # extract all categories and save in dictionary
    categories = {}
    for category in data:
      categories[category.id] = category.type
    
    # create HTTP 404 error (not found)
    if (len(categories) == 0) or (total_questions == 0):
      abort(404)
    
    # return data
    return jsonify({
      'success': True,
      'questions': current_questions,
      'total_questions': total_questions,
      'categories': categories
    })

  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question 
  will be removed.
  This removal will persist in the database and when you refresh the page. 
  ---- Done ----
  '''
  @app.route('/questions/<int:id>', methods=['DELETE'])
  def delete_question(id):
    '''
    API endpoint to DELETE a specific questions from the database

    Input: 
      - id (integer: ID of question to delete)
    
    Output:
      - success (boolean: information whether the request was successful)
      - deleted_question (integer: ID of deleted question)
    '''
    try:
      # get question with specific ID via database query
      question = Question.query.get(id)

      # create HTTP 404 error (not found) in case id is not in the database
      if question is None:
        abort(404)
      
      # delete question
      question.delete()

      return jsonify({
        'success': True,
        'deleted_question': id
      })
    except:
      # create HTTP 422 error in case request is unprocessable
      abort(422)

  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  ---- Done ----
  '''
  @app.route('/questions', methods=['POST'])
  def create_question():
    '''
    API endpoint to create (POST) a new question in the database

    Input: 
      - None
    
    Output:
      - success (boolean: information whether the request was successful)
      - created_question (integer: ID of created question)
      - questions (dictionary: paginated questions in database)
      - total_questions (integer: number of total questions)
    '''
    # get data from POST request as JSON
    data = request.get_json()
    # get each column value of the new question
    question = data.get('question')
    answer = data.get('answer')
    category = data.get('category')
    difficulty = data.get('difficulty')

    # create HTTP 422 error in case request is unprocessable (missing values)
    if ((question is None) or 
        (answer is None) or 
        (category is None) or
        (difficulty is None)):
      abort(422)
    
    try:
      # create new instance of Question
      new_question = Question(
        question = question,
        answer = answer,
        category = category,
        difficulty = difficulty
      )

      # insert new question into database
      new_question.insert()

      # get all questions via database query
      questions = Question.query.all()
      # get total number of questions in database
      total_questions = len(questions)
      # paginate questions
      current_questions = paginate_questions(request, questions)

      return jsonify({
        'success': True,
        'created_question': new_question.id,
        'questions': current_questions,
        'total_questions': total_questions
      })
    except:
      # create HTTP 422 error in case request is unprocessable
      abort(422)

  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  ---- Done ----
  '''
  @app.route('/questions/search', methods=['GET','POST'])
  def search_questions():
    '''
    API endpoint to get questions based on a search term from the database

    Input: 
      - None
    
    Output:
      - success (boolean: information whether the request was successful)
      - questions (dictionary: paginated questions that include search term)
      - total_questions (integer: number of found questions)
    '''
    # get search term (string) from request
    data = request.get_json()
    if(data['searchTerm']):
      search_term = data['searchTerm']
    
    selection = Question.query.filter(
      Question.question.ilike('%'+search_term+'%')).all()

    # create HTTP 404 error (not found) in case there are no questions
    if selection == []:
      abort(404)
    
    # paginate selection
    questions = paginate_questions(request, selection)
    total_questions = len(questions)

    return jsonify({
      'success': True,
      'questions': questions,
      'total_questions': total_questions
    })

  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  ---- Done ----
  '''
  @app.route('/categories/<int:id>/questions', methods=['GET'])
  def get_questions_by_category(id):
    '''
    API endpoint to get questions based on category from the database

    Input: 
      - id (integer: id of category)
    
    Output:
      - success (boolean: information whether the request was successful)
      - questions (dictionary: paginated questions that belong to category)
      - total_questions (integer: number of related questions)
    '''
    # get category by id
    category = Category.query.get(id)
    
    # create HTTP 404 error (not found) in case category is not found
    if category is None:
      abort(404)
    
    # filter questions by category and paginate the output
    try:
      questions = Question.query.filter_by(category=category.id).all()
      current_questions = paginate_questions(request, questions)
      total_questions = len(current_questions)

      return jsonify({
        'success':True,
        'questions': current_questions,
        'total_questions': total_questions,
        'current_category': category.type
      })
    except:
      # create HTTP 500 error (internal server error) in case filtering failed
      abort(500)

  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  ---- Done ----
  '''
  @app.route('/quizzes', methods=['POST'])
  def get_quiz_question():
    '''
    API endpoint to get a random question by category from the database 
    to play the quiz

    Input: 
      - None
    
    Output:
      - success (boolean: information whether the request was successful)
      - question (dictionary: formatted random question from database)
    '''
    try:
      # get category and previous question from request
      data = request.get_json()
      category = data.get('quiz_category')
      previous_questions = data.get('previous_questions')

      # create a selection of questions based on chosen category
      if category['id'] == 0:
        # get questions from all categories and avoid previous questions
        questions = Question.query.filter(
          Question.id.notin_(previous_questions)
          ).all()
      else:
        # get questions from specific category and avoid previous questions
        questions = Question.query.filter(
          Question.id.notin_(previous_questions),
          Question.category == category['id']
          ).all()

      # get random question from selection if there are entries available
      question = None
      if(questions):
        question = random.choice(questions)

      return jsonify({
        'success': True,
        'question': question.format()
      })
    except:
      # create HTTP 422 error in case request is unprocessable
      abort(422)

  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422.
  ---- Done ---- 
  '''
  @app.errorhandler(400)
  def bad_request(error):
    '''
    Error handler HTTP status code 400 Bad Request:
    The server cannot process the request due to an apparent client errors.

    Input: 
      - error
    
    Output:
      - success (boolean: information whether the request was successful)
      - error (integer: HTTP status code)
      - message (string: error message)
    '''
    return( 
        jsonify({
          'success': False, 
          'error': 400,
          'message': 'Bad request'
        }),
        400
    )

  @app.errorhandler(404)
  def not_found(error):
    '''
    Error handler HTTP status code 404 Not found:
    The requested resource could not be found. 

    Input: 
      - error
    
    Output:
      - success (boolean: information whether the request was successful)
      - error (integer: HTTP status code)
      - message (string: error message)
    '''
    return( 
        jsonify({
          'success': False, 
          'error': 404,
          'message': 'Resource not found'
        }),
        404
    )
  
  @app.errorhandler(422)
  def unprocessable(error):
    '''
    Error handler HTTP status code 422 Unprocessable Entity:
    The request was unable to be followed due to semantic errors. 

    Input: 
      - error
    
    Output:
      - success (boolean: information whether the request was successful)
      - error (integer: HTTP status code)
      - message (string: error message)
    '''
    return( 
        jsonify({
          'success': False, 
          'error': 422,
          'message': 'Request cannot be processed'
        }),
        422
    )

  @app.errorhandler(500)
  def internal_server_error(error):
    '''
    Error handler HTTP status code 500 Internal Server Error:
    A generic error message, given when an unexpected condition was 
    encountered and no more specific message is suitable.

    Input: 
      - error
    
    Output:
      - success (boolean: information whether the request was successful)
      - error (integer: HTTP status code)
      - message (string: error message)
    '''
    return( 
        jsonify({
          'success': False, 
          'error': 500,
          'message': 'Internal Server Error'
        }),
        500
    )

  return app

    