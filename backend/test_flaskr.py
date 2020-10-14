import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        # TODO: connect to a local postgresql database: EDIT USER AND PASSWORD
        self.database_user = 'postgres'
        self.database_password = 'admin'
        self.database_server = 'localhost:5432'
        self.database_path = "postgres://{}:{}@{}/{}".format(self.database_user, self.database_password, self.database_server, self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
        
        self.new_question = {
            'question': 'Test Question',
            'answer': 'Test Answer',
            'category': '1',
            'difficulty': 1
        }

        self.incomplete_question = {
            'question': 'Test Question',
            'answer': 'Test Answer',
            'category': '1',
            #'difficulty': 1
        }

    
    def tearDown(self):
        """Executed after reach test"""
        pass


    # Tests

    def test_200_get_categories_success(self):
        res = self.client().get('/api/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['categories'])

    def test_200_get_paginated_questions_success(self):
        res = self.client().get('/api/questions?page=1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['categories']))
        self.assertIsNone(data['current_category'])


    def test_404_get_questions_beyound_page(self):
        res = self.client().get('/api/questions?page=100000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Resource Not Found')

    def test_200_delete_question_success(self):
        last_question = Question.query.order_by(Question.id.desc()).first()
        id = last_question.id
        res = self.client().delete('/api/questions/'+str(id))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['deleted_question_id'],id)

    def test_404_delete_unexisting_question(self):
        res = self.client().delete('/api/questions/1000000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Resource Not Found')
    
    def test_405_delete_without_question_id(self):
        res = self.client().delete('/api/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Method Not Allowed')

    def test_200_add_question_success(self):
        res = self.client().post('/api/questions', json= self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['new_question_id'])
    
    def test_400_add_question_without_json_body(self):
        res = self.client().post('/api/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Bad Request')
    
    def test_405_add_question_with_nonsenes_extra_parameter(self):
        res = self.client().post('/api/questions/12', json= self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Method Not Allowed')

    def test_422_add_question_with_incomplete_fields(self):
        res = self.client().post('/api/questions', json= self.incomplete_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Unprocessable')

    def test_200_get_questions_by_category(self):
        res = self.client().get('/api/categories/1/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['current_category'])
    
    def test_404_get_questions_by_unexisting_category(self):
        res = self.client().get('/api/categories/10000/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Resource Not Found')
    
    def test_200_search_for_question(self):
        res = self.client().post('/api/questions', json= {'searchTerm': 'what'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_questions'])
        self.assertIsNone(data['current_category'])
    
    def test_400_search_for_question_no_json_provided(self):
        res = self.client().post('/api/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], "Bad Request")
    
    def test_200_search_for_question_without_results(self):
        res = self.client().post('/api/questions', json= {'searchTerm': 'dsjdsoewjdaslqw'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(len(data['questions']), 0)
        self.assertEqual(data['total_questions'], 0)
        self.assertIsNone(data['current_category'])

    def test_200_quiz_get_random_question_without_category(self):
        res = self.client().post('/api/quiz', json = {
            "quiz_category": {
                "id": 0
            },
            "previous_questions": []
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['question'])
        self.assertTrue(data['question']['question'])
    
    
    def test_200_quiz_get_random_question_with_category(self):
        res = self.client().post('/api/quiz', json = {
            "quiz_category": {
                "id": 1
            },
            "previous_questions": []
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['question'])
        self.assertTrue(data['question']['question'])
        self.assertEqual(data['question']['category'], 1)
    
    def test_400_quiz_no_json_body_provided(self):
        res = self.client().post('/api/quiz')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Bad Request')

    def test_400_quiz_incomplete_json_body_provided(self):
        res = self.client().post('/api/quiz', json = {
            "previous_questions": []
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Bad Request')

    def test_404_quiz_unexisting_category_provided(self):
        res = self.client().post('/api/quiz', json = {
            "quiz_category": {
                "id": 100001
            },
            "previous_questions": []
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Resource Not Found')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()