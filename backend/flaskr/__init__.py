import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
import sys

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  cors = CORS(app, resources={
    r"/api/*": {"origins": "*"}
    })


  @app.after_request
  def after_request(response):
    response.headers.add(
      'Access-Control-Allow-Headers',
      'Content-Type,Authorization,true'
    )
    response.headers.add(
      'Access-Control-Allow-Methods',
      'GET,POST,DELETE,OPTIONS'
    )

    return response
  


  #Utilities Methods
   
  def paginate_questions(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page-1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    f_questions = [question.format() for question in selection[start:end]]

    return f_questions

  def reformat_categories_for_frontend(f_categories):
    ff_categories = {}
    for d_category in f_categories:
      ff_categories[d_category['id']] = d_category['type']
    
    return ff_categories


  #API Endpoints
  @app.route('/api')
  def index():
    return jsonify(
      success = True,
      message = 'Hello To Trivia API, Please Refer to the Documentation for more information'
    )

  @app.route('/api/categories')
  def get_categories():
    try:
      categories = Category.query.order_by('id').all()
      f_categories = [category.format() for category in categories]
      ff_categories = reformat_categories_for_frontend(f_categories)
    except:
      print(sys.exc_info())
      abort(422)
    return jsonify(
      success = True,
      categories = ff_categories
    )

  @app.route('/api/questions')
  def get_questions():
    try:
      questions = Question.query.order_by('id').all()
      f_questions = paginate_questions(request, questions)

      categories = Category.query.order_by('id').all()
      f_categories = [category.format() for category in categories]
      ff_categories = reformat_categories_for_frontend(f_categories)
    except:
      print(sys.exc_info())
      abort(422)     
    if len(f_questions) == 0 or len(ff_categories) == 0:
      abort(404)
    return jsonify(
      success = True,
      questions = f_questions,
      total_questions = len(questions),
      categories = ff_categories,
      current_category = None
    )

  @app.route('/api/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):
    try:
      question = Question.query.filter(Question.id == int(question_id)).one_or_none()
    except:
      print(sys.exc_info())
      abort(422)
    if question is None:
      abort(404)
    question.delete()
    return jsonify(
      success = True,
      deleted_question_id = question_id
    )

  @app.route('/api/questions', methods=['POST'])
  def add_question_or_search():
    body = request.get_json()
    if not body:
      abort(400)

    question_field = body.get('question', None)
    answer_field = body.get('answer', None)
    difficulty_field = body.get('difficulty', None)
    category_field = body.get('category', None)
    search = body.get('searchTerm', None)

    if search:
      try:
        questions = Question.query.order_by(Question.id).filter(Question.question.ilike('%{}%'.format(search))).all()
        f_questions = paginate_questions(request, questions)
      except:
        print(sys.exc_info())
        abort(422)
      return jsonify(
        success = True,
        questions = f_questions,
        total_questions = len(questions),
        current_category = None
      )

    else:

      if not (question_field and answer_field and difficulty_field and category_field):
        abort(422)
        
      try:
        new_question = Question(
          question = question_field,
          answer = answer_field,
          category = category_field,
          difficulty = difficulty_field
        )
        new_question.insert()
        
      except:
        print(sys.exc_info())
        abort(422)
      
      return jsonify(
        success = True,
        new_question_id = new_question.id
      )

  @app.route('/api/categories/<int:category_id>/questions')
  def get_questions_by_category(category_id):
    try:
      category = Category.query.filter(Category.id == category_id).one_or_none()
      questions = Question.query.filter(Question.category == str(category_id)).all()
    except:
      abort(422)
    
    if len(questions) == 0 or category is None:
      abort(404)
    
    f_questions = paginate_questions(request, questions)

    return jsonify(
      success = True,
      questions = f_questions,
      total_questions = len(questions),
      current_category = category.type
    )
    
  @app.route('/api/quiz', methods=['POST'])
  def quiz():
    body = request.get_json()

    if body is None:
      abort(400)
    
    if 'quiz_category' not in body:
      abort(400)
    
    if 'previous_questions' not in body:
      abort(400)
    
    quiz_category = body.get('quiz_category', None)
    previous_questions = body.get('previous_questions', None)
    category_id = quiz_category['id']   

    try:
      if category_id == 0:
        questions = Question.query.all()
      else:
        questions = Question.query.filter(Question.category == category_id).all()
    except:
      print(sys.exc_info())
      abort(422)
    
    if not questions:
      abort(404)
    
    selection_pool = []
    selected_question = None
    for q in questions:
      if q.id not in previous_questions:
        selection_pool.append(q)
    
    if selection_pool:
      selected_question = random.choice(selection_pool).format()

    return jsonify(
      success = True,
      question = selected_question
    )
  


  #Error Handlers

  @app.errorhandler(400)
  def bad_request(error):
    return jsonify(
      success = False,
      error = 400,
      message = 'Bad Request'
    ), 400

  @app.errorhandler(404)
  def not_found(error):
    return jsonify(
      success = False,
      error = 404,
      message = 'Resource Not Found'
    ), 404

  @app.errorhandler(405)
  def method_not_allowed(error):
    return jsonify(
      success = False,
      error = 405,
      message = 'Method Not Allowed'
    ), 405

  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify(
      success = False,
      error = 422,
      message = 'Unprocessable'
    ), 422


  return app

    