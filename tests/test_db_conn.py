from .base import *

def test_delete_command_users(sign_up_user):

    user = conn.get_user(user_data1['username'])

    conn.delete_entry('users', user[3])
    user = conn.get_user(user_data1['username'])

    assert user is None
    assert 'success' in sign_up_user.json

def test_delete_command_answers(init_db, insert_new_records):
    
    ans = conn.query_all('answers')
    ans_id = ans[0][3]
    conn.delete_entry('answers', ans_id)
    ans = conn.query_all('answers')
    assert ans[0][3] != ans_id


    