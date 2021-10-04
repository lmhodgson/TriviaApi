import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from backend.flaskr.models import setup_db, Question


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}/{}"\
            .format('postgres:ShushPaul123@localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_questions(self):
        res = self.client().get("/questions")
        data = json.loads(res.data)

        self.assertEqual(200, res.status_code)
        self.assertTrue(data["success"])
        self.assertTrue(data['total_questions'])
        self.assertIsNotNone(data['questions'])
        self.assertIsNotNone(data['categories'])

    def test_get_questions_404_invalid_page(self):
        res = self.client().get('/questions?page=20')
        data = json.loads(res.data)

        self.assertEqual(404, res.status_code)
        self.assertFalse(data['success'])
        self.assertEqual('Resource Not Found', data['message'])

    def test_get_categories(self):
        res = self.client().get("/categories")
        data = json.loads(res.data)

        self.assertEqual(200, res.status_code)
        self.assertTrue(data["success"])
        self.assertIsNotNone(data["categories"])

    def test_get_categories_404_null_category(self):
        res = self.client().get('/categories/10')
        data = json.loads(res.data)

        self.assertEqual(404, res.status_code)
        self.assertFalse(data['success'])
        self.assertEqual('Resource Not Found', data['message'])

    def test_delete_question(self):
        question = Question(question='Test Question', answer='Test Answer',
                            difficulty=1, category=1)
        question.insert()
        question_id = question.id

        res = self.client().delete(f'/questions/{question_id}')
        data = json.loads(res.data)

        question = Question.query.filter(
            Question.id == question_id).one_or_none()

        self.assertEqual(200, res.status_code)
        self.assertTrue(data['success'])
        self.assertIsNone(question)

    def test_delete_question_404_null_question(self):
        res = self.client().delete('/questions/hello')
        data = json.loads(res.data)

        self.assertEqual(404, res.status_code)
        self.assertFalse(data['success'])
        self.assertEqual('Resource Not Found', data['message'])

    def test_search_questions(self):
        request = {'searchTerm': 'a'}
        res = self.client().post('/questions/search', json=request)
        data = json.loads(res.data)

        self.assertEqual(200, res.status_code)
        self.assertTrue(data['success'])
        self.assertIsNotNone(data['questions'])
        self.assertIsNotNone(data['total_questions'])

    def test_search_questions_404(self):
        request = {'searchTerm': 'hello'}
        res = self.client().post('/questions/search', json=request)
        data = json.loads(res.data)

        self.assertEqual(404, res.status_code)
        self.assertFalse(data['success'])
        self.assertEqual('Resource Not Found', data['message'])

    def test_add_question(self):
        request = {
            'question': 'this is a new question',
            'answer': 'this is a new answer',
            'difficulty': 1,
            'category': 1
        }
        res = self.client().post('/questions', json=request)
        data = json.loads(res.data)

        self.assertEqual(200, res.status_code)
        self.assertTrue(data['success'])
        self.assertIsNotNone(data['questions'])
        self.assertTrue(data['total_questions'])

    def test_add_question_422_invalid_request(self):
        request = {
            'question': 'this is a new question',
            'answer': 'this is a new answer',
            'difficulty': 1
        }
        res = self.client().post('/questions', json=request)
        data = json.loads(res.data)

        self.assertEqual(422, res.status_code)
        self.assertFalse(data['success'])
        self.assertEqual('Unprocessable Entity', data['message'])

    def test_get_questions_per_category(self):
        res = self.client().get("/categories/1/questions")
        data = json.loads(res.data)

        self.assertEqual(200, res.status_code)
        self.assertTrue(data["success"])
        self.assertTrue(data['total_questions'])
        self.assertIsNotNone(data['questions'])

    def test_get_questions_404_invalid_category(self):
        res = self.client().get('/categories/hello/questions')
        data = json.loads(res.data)

        self.assertEqual(404, res.status_code)
        self.assertFalse(data['success'])
        self.assertEqual('Resource Not Found', data['message'])

    def test_get_random_quiz_question(self):
        request = {
            'previous_questions': [],
            'quiz_category': {'type': 'Entertainment', 'id': 5}
        }

        res = self.client().post('quizzes', json=request)
        data = json.loads(res.data)

        self.assertEqual(200, res.status_code)
        self.assertTrue(data["success"])
        self.assertIsNotNone(data["question"])
        self.assertTrue(data["total_questions"])

    def test_get_random_quiz_question_404_invalid_category(self):
        request = {
            'previous_questions': [],
            'quiz_category': {'type': 'Entertainment', 'id': 10}
        }

        res = self.client().post('quizzes', json=request)
        data = json.loads(res.data)

        self.assertEqual(404, res.status_code)
        self.assertFalse(data['success'])
        self.assertEqual('Resource Not Found', data['message'])


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()