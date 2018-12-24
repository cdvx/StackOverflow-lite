import os

import psycopg2

HEROKU = os.environ.get('HEROKU')

DATABASE_URL = os.environ['DATABASE_URL']

class DatabaseConnection(object):
    def __init__(self):
        if os.getenv('APP_SETTINGS') == "testing":
            self.dbname = "test_db2"
        elif DATABASE_URL == HEROKU:
            try:
                self.connection = psycopg2.connect(DATABASE_URL, sslmode='require')
                self.connection.autocommit = True
                self.cursor = self.connection.cursor()
                self.last_ten_queries = []
            except:
                print("cannot connect to Heroku database")

        else:
            self.dbname = "clvx" 

        try:
            print("db is>>>", self.dbname)
            self.connection = psycopg2.connect(dbname=f"{self.dbname}", user='postgres', host='localhost', password='Tesxting', port='5432')
            self.connection.autocommit = True
            self.cursor = self.connection.cursor()
            self.last_ten_queries = []
        except:
            print("Cannot connect to database.")   

    def create_Users_table(self):
        try:
            self.tablename = 'users'
            create_table_command = """CREATE TABLE IF NOT EXISTS users(
                id serial PRIMARY KEY,
                username varchar(100) NOT NULL,
                email varchar(100) NOT NULL,
                password_hash varchar(200) NOT NULL,
                user_id varchar(150) NOT NULL
            );"""
            self.cursor.execute(create_table_command)
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def create_Questions_table(self):
        try:
            self.tablename = 'questions'
            create_table_command = """CREATE TABLE IF NOT EXISTS questions(
                id serial PRIMARY KEY,
                topic varchar(100) NOT NULL,
                body varchar(600) NOT NULL,
                author varchar(100) NOT NULL,
                question_id varchar(150) NOT NULL
            );"""
            self.cursor.execute(create_table_command)
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def create_Answers_table(self):
        try:
            self.tablename = 'answers'
            create_table_command = """CREATE TABLE IF NOT EXISTS answers(
                id serial PRIMARY KEY,
                Qn_Id varchar(150) NOT NULL,
                body varchar(600) NOT NULL,
                answer_id varchar(150) NOT NULL,
                author varchar(100) NOT NULL,
                prefered boolean
            );"""
            self.cursor.execute(create_table_command)
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def insert_new_record(self, tablename, data):
        tables = ['users', 'questions', 'answers']
        try:
            if tablename == tables[0]:
                insert_command = """INSERT INTO users(
                    username,
                    email,
                    password_hash,
                    user_id
                ) VALUES(
                    %s,
                    %s,
                    %s,
                    %s
                );"""
                self.cursor.execute(insert_command, (
                    data['username'],
                    data['email'],
                    data['password'],
                    data['user_id'])
                 )
            elif tablename == tables[1]:
                insert_command = """INSERT INTO questions(
                    topic,
                    body,
                    author,
                    question_id
                ) VALUES(
                    %s,
                    %s,
                    %s,
                    %s
                );"""
                self.cursor.execute(insert_command, (
                    data['topic'],
                    data['body'],
                    data['author'],
                    data['questionId'])
                )
            elif tablename == tables[2]:
                insert_command = """INSERT INTO answers(
                    Qn_Id,
                    body,
                    answer_id,
                    author,
                    prefered
                ) VALUES(
                    %s,
                    %s,
                    %s,
                    %s,
                    %s
                );"""
                self.cursor.execute(insert_command, (
                    data['Qn_Id'],
                    data['body'],
                    data['answerId'],
                    data['author'],
                    data['prefered'])
                )
            else:
                if tablename not in tables:
                    msg = f"User table {tablename} does not exit."
                    return msg
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def query_all(self, tablename):
        queries = []
        try:
            self.cursor.execute(f"SELECT * FROM {tablename}")
            items = self.cursor.fetchall()
            if items:
                for item in items:
                    queries.append(item)
                    if len(self.last_ten_queries) == 11:
                        self.last_ten_queries.pop()
                        self.last_ten_queries.append(item)
                return queries
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        else:
            return queries

    def update_question(self, new_topic, new_body, questionId):
        try:    
            update_command = """UPDATE questions SET topic = %s, body = %s 
                                WHERE question_id = %s"""
            self.cursor.execute(update_command, (new_topic, new_body, questionId))
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def update_answer(self, answerId):
        try:    
            update_command = """UPDATE answers SET prefered = %s WHERE answer_id = %s"""
            self.cursor.execute(update_command, (True, str(answerId)))
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    
    def delete_entry(self, tablename, id_value):
        try:
            if tablename == 'questions':
                delete_command = """DELETE FROM questions
                                    WHERE question_id = %s"""
                self.cursor.execute(delete_command, (id_value, ))

            if tablename == 'answers':
                delete_command = """DELETE FROM answers
                                    WHERE answer_id = %s"""
                self.cursor.execute(delete_command, (id_value, ))

            if tablename == 'users':
                delete_command = """DELETE FROM users
                                    WHERE user_id = %s"""
                self.cursor.execute(delete_command, (id_value, ))
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
    
    def drop_table(self, tablename):
        
        try:
            drop_table_command = f"DROP TABLE {tablename} CASCADE"
            self.cursor.execute(drop_table_command)
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)


conn = DatabaseConnection()
#conn.drop_table('answers')
conn.create_Answers_table()
#conn.drop_table('users')
conn.create_Users_table()
#conn.drop_table('questions')
conn.create_Questions_table()
