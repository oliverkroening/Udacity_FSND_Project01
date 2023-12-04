import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from setting import DB_PASSWORD, DB_NAME_TEST, DB_USER
from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.database_name = DB_NAME_TEST
        self.database_path = "postgresql://{}:{}@{}/{}".format(
            DB_USER, DB_PASSWORD, 'localhost:5432', self.database_name)
        self.app = create_app(self.database_path)
        self.client = self.app.test_client
        #setup_db(self.app, self.database_path)

        # binds the app to the current context
        # with self.app.app_context():
        #     self.db = SQLAlchemy()
        #     self.db.init_app(self.app)
        #     # create all tables
        #     self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and 
    for expected errors.
    ---- Done ----
    """

    ### ---------------------------------------------
    ### Tests according to function: get_categories()
    ### ---------------------------------------------

    def test_get_categories(self):
        '''
        Positive test function for get_categories() 
        at API endpoint '/categories' by perfoming a GET request
        
        - supposed result: List of categories
        '''
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])
    
    ### --------------------------------------------
    ### Tests according to function: get_questions()
    ### --------------------------------------------
    
    def test_get_questions(self):
        '''
        Positive test function for get_questions() 
        at API endpoint '/questions' by perfoming a GET request
        
        - supposed result: List of paginated questions
        '''
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
    
    def test_get_questions_404_invalid_page_numbers(self):
        '''
        Negative test function for get_questions() 
        at API endpoint '/questions' by perfoming a GET request due to
        invalid page numbers
        
        - supposed result: HTTP 404 error
        '''
        res = self.client().get('/questions?page=1000')
        data = json.loads(res.data)

        self.assertEqual(data['success'], False)
        self.assertTrue(data['error'], 404)
    
    ### ----------------------------------------------
    ### Tests according to function: delete_question()
    ### ----------------------------------------------

    def test_delete_question(self):
        '''
        Positive test function for delete_question() 
        at API endpoint '/questions/<int:id>' by perfoming a DELETE request
        
        - supposed result: question_id 10 is successfully deleted from database
        '''
        res = self.client().delete('/questions/10')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted_question'], 10)

    def test_delete_question_404_not_found(self):
        '''
        Negative test function for get_questions() 
        at API endpoint '/questions' by perfoming a GET request due to
        question id is not available
        
        - supposed result: HTTP 404 error
        '''
        res = self.client().delete('/questions/100')
        data = json.loads(res.data)

        self.assertEqual(data['success'], False)
        self.assertTrue(data['error'], 404)
    
    ### -----------------------------------------------
    ### Tests according to function: create_questions()
    ### -----------------------------------------------
    
    def test_create_question(self):
        '''
        Positive test function for create_question() 
        at API endpoint '/questions' by perfoming a POST request
        
        - supposed result: new question is successfully inserted into database
        '''
        new_question = {
        'question': 'What is the capitol of Germany?',
        'answer': 'Berlin',
        'category': '3',
        'difficulty': 1,
        }

        res = self.client().post('/questions', json=new_question)
        data = json.loads(res.data)

        self.assertEqual(data['success'], True)
        self.assertTrue(data['created_question'])
    
    def test_create_question_422_unprocessable(self):
        '''
        Negative test function for create_question() 
        at API endpoint '/questions' by perfoming a POST request due to
        missing values
        
        - supposed result: HTTP 422 error
        '''
        new_question = {
        'question': 'Who painted Mona Lisa?',
        'category': '2',
        'difficulty': 1,
        }

        res = self.client().post('/questions', json=new_question)
        data = json.loads(res.data)

        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 422)
        self.assertEqual(data['message'], "Request cannot be processed")
    
    ### -----------------------------------------------
    ### Tests according to function: search_questions()
    ### -----------------------------------------------

    def test_search_questions(self):
        '''
        Positive test function for search_questions() 
        at API endpoint '/questions/search' by perfoming a POST request
        
        - supposed result: new question is successfully inserted into database
        '''
        res = self.client().post('questions/search', json={"searchTerm": "title"})
        data = json.loads(res.data)

        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])

    def test_seach_questions_404_unavailable_question(self):
        '''
        Negative test function for search_questions() 
        at API endpoint '/questions/search' by perfoming a POST request due to
        unavailable search results
        
        - supposed result: HTTP 404 error
        '''
        res = self.client().post('questions/search', json={"searchTerm": "abcde"})
        data = json.loads(res.data)

        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], "Resource not found")
    
    ### -------------------------------------------------------
    ### Tests according to function: get_question_by_category()
    ### -------------------------------------------------------
    
    def test_get_question_by_category(self):
        '''
        Positive test function for search_questions() 
        at API endpoint '/categories/<int:id>/questions' 
        by perfoming a GET request
        
        - supposed result: list of questions of a specific category
        '''
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])

    def test_get_question_by_category_404_not_found(self):
        '''
        Negative test function for search_questions() 
        at API endpoint '/categories/<int:id>/questions' 
        by perfoming a GET request due to
        category input out of range
        
        - supposed result: HTTP 404 error
        '''
        res = self.client().get('/categories/100/questions')
        data = json.loads(res.data)

        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], "Resource not found")

    ### ------------------------------------------------
    ### Tests according to function: get_quiz_question()
    ### ------------------------------------------------
    
    def test_get_quiz_question(self):
        '''
        Positive test function for get_quiz_question() 
        at API endpoint '/quizzes' by perfoming a POST request
        
        - supposed result:  random question of category 5 and 
                            may not be id 2 or 4
        '''
        input_data = {
            'previous_questions':[2, 4],
            'quiz_category': {
                'id': 5,
                'type': 'Entertainment'
            }
        }
        res = self.client().post('/quizzes', json=input_data)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])
        self.assertNotEqual(data['question']['id'], 2)
        self.assertNotEqual(data['question']['id'], 4)
        self.assertEqual(data['question']['category'], 5)

    def test_get_quiz_question_422_unprocessable(self):
        '''
        Negative test function for get_quiz_question() 
        at API endpoint '/quizzes' by perfoming a POST request due to
        missing quiz category
        
        - supposed result: HTTP 422 error
        '''
        input_data = {
            'previous_questions':[2, 4],
        }
        res = self.client().post('/quizzes', json=input_data)
        data = json.loads(res.data)

        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 422)
        self.assertEqual(data['message'], "Request cannot be processed")

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()