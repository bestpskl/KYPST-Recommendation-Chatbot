from flask import jsonify
from system import Configurator
from user import User
from typing import List, Set
import json, os, sys
import datetime

def user(request):
    print('INFO:', {'request': request.json})
    config = Configurator('./private/config.json')
    user = User(config)
    ''' Create new user '''
    print('request.method')
    print(request.method)
    if request.method == 'POST':
        user_id = request.json['source']['user_id']
        display_name = request.json['display_name']
        user.user_create(user_id=user_id, display_name=display_name)
        return jsonify({'code': 200})
    if request.method == 'GET':
        user_id = request.args.get('user_id')
        print(user_id)
        return user.user_retrieve(user_id=user_id) 
    if request.method == 'PUT':
        print('data')
        data = json.loads(request.data)
        print(data)
        user_id = data['user_id']
        sum_score = data['sum_score']
        investment_type = data['investment_type']
        last_question = data['last_question']
        count_of_assessment = data['count_of_assessment']
        finished_assessment_date = data['finished_assessment_date']
        status = data['status']
        result = user.user_update(user_id=user_id, sum_score=sum_score, investment_type=investment_type,
        last_question=last_question, count_of_assessment=count_of_assessment, finished_assessment_date=finished_assessment_date, 
        status=status)
        return jsonify({'code': 200})
    if request.method == 'DELETE':
        user_id = request.args.get('user_id')
        print(user_id)
        user.user_delete(user_id=user_id)
        return jsonify({'code': 200})
