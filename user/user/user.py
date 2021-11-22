from typing import List
from system import Configurator
from db import CloudSql
from pandas import DataFrame
import json
import time  

class User:


    def __init__(self, configurator: Configurator):
        self.configurator = configurator
        self.database = self.configurator.get('cloud_sql.database')
        self.table = self.configurator.get('cloud_sql.table')

    def user_create(self, user_id:str, display_name:str) -> List:
        SQL = '''
            INSERT INTO `{table}` (user_id, display_name) VALUES ('{user_id}', '{display_name}');
        '''
        db = CloudSql(self.configurator)
        query = SQL.format(database=self.database, table=self.table, user_id=user_id, display_name=display_name)
        print('query'+ query)
        result = db.query(sql=query)
        print(result)
    
    def user_retrieve(self, user_id:str) -> List:
        print('user_retrieve')
        SQL = '''
            SELECT * FROM `{table}` WHERE user_id = '{user_id}';
        '''
        db = CloudSql(self.configurator)
        query = SQL.format(database=self.database, table=self.table, user_id=user_id)
        print('query'+ query)
        result = db.query_df(sql=query)
        print("------result-------")
        print(result)
        if result.empty: return {}
        result = result.to_dict()
        for key in result:
            result[key] = result[key][0]
        print(result)
        return result

    def user_update(self, user_id:str, sum_score:int, investment_type:int, last_question:int, count_of_assessment:int, finished_assessment_date:time, status:int) -> List:
        print('user_update')
        SQL = '''
            UPDATE `{table}` 
            SET sum_score = '{sum_score}', investment_type = '{investment_type}', last_question = '{last_question}', 
            count_of_assessment = '{count_of_assessment}', finished_assessment_date = '{finished_assessment_date}',
            status = '{status}'
            WHERE user_id = '{user_id}';
        '''
        db = CloudSql(self.configurator)
        query = SQL.format(database=self.database, table=self.table, user_id=user_id, sum_score=sum_score, investment_type=investment_type,
        last_question=last_question, count_of_assessment=count_of_assessment, finished_assessment_date=finished_assessment_date, status=status)
        print('query'+ query)
        result = db.query(sql=query)
        print("------result-------")
        print(result)


    def user_delete(self, user_id:str) -> List:
        print('user_delete')
        SQL = '''
            UPDATE `{table}` SET status = 0 WHERE user_id = '{user_id}';
        '''
        db = CloudSql(self.configurator)
        query = SQL.format(database=self.database, table=self.table, user_id=user_id)
        print('query'+ query)
        result = db.query(sql=query)
        print("------result-------")
        print(result)

