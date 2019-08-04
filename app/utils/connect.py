import os

import psycopg2
from config import Config
from .sql_queries import SQL


DATABASE_URL = Config.POSTGREST_DATABASE_URI
DB_NAME = Config.DB_NAME


class DatabaseConnection:
    """Class to manage database connection"""

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super(DatabaseConnection, cls).__new__(cls)
        return cls.instance

    def __init__(self, url=None):
        self.db_url = url
        if self.db_url:
            try:
                self.connection = psycopg2.connect(self.db_url, sslmode='allow')
                self.connection.autocommit = True
                self.cursor = self.connection.cursor()
            except Exception as e: #pragma: no cover
                print("Cannot connect to database", e)
        else: #pragma: no cover
            print('Could not connect to database\nReason: Database url not provided!')

class DbMethods:
    """Class with database actions"""
    
    def create_Users_table(self):
        DbManager.excute_sql(SQL['create_users_table'], tablename='users')

    def create_Questions_table(self):
        DbManager.excute_sql(SQL['create_questions_table'], tablename='questions')

    def create_Answers_table(self):
        DbManager.excute_sql(SQL['create_answers_table'], tablename='answers')

    def insert_new_record(self, tablename, data):
        if tablename == 'users':
            DbManager.excute_sql(
                SQL['insert_into_users'],
                tablename='users',
                values=(
                    data['username'],
                    data['email'],
                    data['password'],
                    data['user_id'],
                ))

        elif tablename == 'questions':
            DbManager.excute_sql(
                SQL['insert_into_questions'],
                tablename='questions',
                values=(
                    data['topic'],
                    data['body'],
                    data['author'],
                    data['questionId']
                ))

        elif tablename == 'answers':
            DbManager.excute_sql(
                SQL['insert_into_answers'],
                tablename='answers',
                values=(
                    data['Qn_Id'],
                    data['body'],
                    data['answerId'],
                    data['author'],
                    data['prefered']
                ))

    def query_all(self, tablename):
        return DbManager.get(SQL['select'], tablename=tablename)


    def get_user(self, username):
        return DbManager.get(SQL['fetch_user'], value=username)

    def get_question(self, question_id):
        return DbManager.get(SQL['get_question'], value=question_id)

    def update_question(self, new_topic, new_body, questionId):
        DbManager.excute_sql(SQL['update_question'], values=(new_topic, new_body, questionId))

    def update_answer(self, answerId):
        DbManager.excute_sql(SQL['update_question'], values=(True, str(answerId)))
    
    def delete_entry(self, tablename, id_value):
        if tablename == 'questions':
            DbManager.excute_sql(SQL['delete_question'], values=(id_value, ))
        elif tablename == 'answers':
            DbManager.excute_sql(SQL['delete_answer'], values=(id_value, ))
        elif tablename == 'users':
            DbManager.excute_sql(SQL['delete_user'], values=(id_value, ))
    
    def drop_table(self, tablename):
        DbManager.excute_sql(SQL['drop'].format(tablename), drop=True)

    def create_all(self):
        self.create_Answers_table()
        self.create_Users_table()
        self.create_Questions_table()
    
    def drop_all(self):
        for table in self.tablenames:
            self.drop_table(table)

class DbManager(DatabaseConnection, DbMethods):
    """Class ro manage database actions"""

    def __init__(self, env, local=None):
        super(DbManager, self).__init__(
            url=DbManager.create_db_url(env, local=local)
        )
        self.tablenames = ['users', 'questions', 'answers']

    @classmethod
    def create_db_url(cls, env, local=None):
        test_db = Config.TEST_DB
        db_name = Config.DB_NAME
        if env in ['testing', 'development']:
            return f"postgresql://localhost/{db_name}" if local \
                else f"postgresql://localhost/{test_db}"
        return Config.POSTGREST_DATABASE_URI

    
    @classmethod
    def excute_sql(cls, sql, tablename=None, values=None, drop=None):
        try:
            if tablename and drop is None:
                cls.instance.tablename = tablename
            cls.instance.cursor.execute(sql, values) if values else cls.instance.cursor.execute(sql)
        except (Exception, psycopg2.DatabaseError) as error: #pragma: no cover
            print(error)

    @classmethod
    def get(cls, sql, tablename=None, value=None):
        try:
            if tablename:
                cls.instance.cursor.execute(sql.format(tablename))
                results = cls.instance.cursor.fetchall()
                return list(results)
            elif value:
                cls.instance.cursor.execute(sql, (value,))
                result = cls.instance.cursor.fetchone()
                return result if result else None
            
        except (Exception, psycopg2.DatabaseError) as error: #pragma: no cover
            print(error)



conn = DbManager(os.getenv('APP_SETTINGS'), local=True)

conn.create_all()
# conn.drop_all
