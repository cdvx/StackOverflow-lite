SQL = {
    "create_users_table": """CREATE TABLE IF NOT EXISTS users(
                            id serial PRIMARY KEY,
                            username varchar(100) NOT NULL,
                            email varchar(100) NOT NULL,
                            password_hash varchar(200) NOT NULL,
                            user_id varchar(150) NOT NULL
                        );""",
    "create_questions_table": """CREATE TABLE IF NOT EXISTS questions(
                                id serial PRIMARY KEY,
                                topic varchar(100) NOT NULL,
                                body varchar(600) NOT NULL,
                                author varchar(100) NOT NULL,
                                question_id varchar(150) NOT NULL
                            );""",
    "create_answers_table": """CREATE TABLE IF NOT EXISTS answers(
                                id serial PRIMARY KEY,
                                Qn_Id varchar(150) NOT NULL,
                                body varchar(600) NOT NULL,
                                answer_id varchar(150) NOT NULL,
                                author varchar(100) NOT NULL,
                                prefered boolean
                            );""",
    "insert_into_users": """INSERT INTO users(
                            username,
                            email,
                            password_hash,
                            user_id
                        ) VALUES(
                            %s,
                            %s,
                            %s,
                            %s
                        );""",
    "insert_into_questions": """INSERT INTO questions(
                                topic,
                                body,
                                author,
                                question_id
                            ) VALUES(
                                %s,
                                %s,
                                %s,
                                %s
                            );""",
    "insert_into_answers": """INSERT INTO answers(
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
                            );""",
    "select": "SELECT * FROM {}",
    "fetch_user": """SELECT username, email, password_hash, user_id
                     FROM users 
                     WHERE username = %s 
                  """ or \
                      """SELECT username, email, password_hash 
                         FROM users 
                         WHERE email = %s 
                  """,
    "update_question": """UPDATE questions SET topic = %s, body = %s 
                        WHERE question_id = %s""",
    "update_answer": """UPDATE answers SET prefered = %s WHERE answer_id = %s""",
    "delete_question": """DELETE FROM questions WHERE question_id = %s""",
    "delete_user": """DELETE FROM users WHERE user_id = %s""",
    "delete_answer": """DELETE FROM answers WHERE answer_id = %s""",
    "drop": "DROP TABLE {} CASCADE",
    "get_question":"""SELECT topic, body, question_id, author
                      FROM questions 
                      WHERE question_id = %s """
}