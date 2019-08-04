from app.routes.imports import *

auth = Blueprint("auth", __name__)

@auth.route('/api/v1/auth/login', methods=['POST'])
def login():

    request_data = request.get_json()
    username, email, password = (
        request_data['username'],
        request_data['email'],
        request_data['password']
    )
    if not request_data:
        raise ValidationError('JSON missing in request!', 400)

    if valid_login_data(request_data):
        
        user = conn.get_user(username or email)
        user = check_password_hash(user[2], password) if user else None
        if not user:
            raise ValidationError('Invalid username or password', status_code=401)

        access_token = create_access_token(
            identity=username,
            fresh=timedelta(minutes=1440)
        )

        msg = {'access_token': f'{access_token}', 'username': username}
        response = make_response(jsonify(msg))
        response.headers.add('Acess-Control-Allow-Origin', origin)
        response.headers.add('Acess-Control-Allow-Headers', 'Content-Type,Authorization')
        return response, 200

    username_or_email = username or email
    not_pass = not password
    all_missing = not_pass and not username_or_email

    all_or_password = all_missing or not_pass

    msg_ = lambda all_or_password, password: 'Please provide email or username, and password to login!' if all_or_password \
        else '{} is required for login!'.format(password.title())
    
    msg = msg_(all_or_password, password)

    raise ValidationError('Password or Email required to login!', status_code=400) \
        if not username_or_email else ValidationError(msg, status_code=400)
        
        

@auth.route('/api/v1/auth/signup', methods=['POST'])
def signup():
    request_data = request.get_json()
    email, username, password, repeat_password = (
        request_data.get('email'),
        str(request_data['username']).strip().split(),
        request_data.get('password'),
        request_data.get('repeat_password')
    )

    if not request_data:
        return jsonify({'message': 'JSON missing in request!'}), 400

    if valid_signup_data(request_data):
        username = username[0] + " " + username[1] if len(username) !=1 else username[0]

        if not valid_username(username) or not valid_email(email):
            raise ValidationError(f'Username: {username} already taken!', 401) \
                if not valid_username(username) else ValidationError(f'Email: {email} already taken!', 401)
        
        passwords_match = password == repeat_password

        if passwords_match:
            user = User(username, email, password)
            conn.insert_new_record('users', user.__repr__())

            response = make_response(jsonify({
                'success': f"{username}'s account created successfully"}))
            response.headers.add('Acess-Control-Allow-Origin', origin)
            response.headers.add('Acess-Control-Allow-Headers', 'Content-Type,Authorization')
            return response, 201
        else:
            raise ValidationError('Passwords do not match!', 401)
                        
    not_all = not password and not username and not email and not repeat_password
    not_pw = repeat_password and username and email and not password
    not_username = repeat_password and not username and email and password
    not_email = repeat_password and username and not email and password
    not_repeat = repeat_password and not username and email and password

    return check_missing_feilds(
        not_all, not_pw,
        not_username,
        not_email,
        not_repeat
    )
    


def check_missing_feilds(*args):
    not_all, not_pw, not_username, not_email, not_repeat = args
    
    if not_all:
        raise ValidationError('Please provide required fields to login!', status_code=400)
    elif not_pw or not_repeat or not_username or not_email:
        mapper = {
            'password': not_pw,
            'repeat_password': not_repeat,
            'username': not_username,
            'email': not_email
        }  
        for key in mapper.keys():
            return_resp(key, mapper.get(key), 400) 
    

def return_resp(field, condition, code):
    if condition:
        msg = '{} field is required!'.format(field.title())
        raise ValidationError(msg, status_code=code)




