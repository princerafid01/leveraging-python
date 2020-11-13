from flask import Flask, request, jsonify, make_response
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
import jwt
import datetime
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = 'thisissecret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/apiAuth'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return jsonify({
                'message': 'Token is missing!'
            }), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = User.query.filter_by(public_id=data['public_id']).first()
        except:
            return jsonify({
                "message": 'Token is invalid!'
            }), 401

        return f(current_user, *args, **kwargs)

    return decorated

# Model


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(50))
    password = db.Column(db.String(80))
    admin = db.Column(db.Boolean)

    def __init__(self, name, password, public_id, admin):
        self.name = name
        self.password = password
        self.public_id = public_id
        self.admin = admin

    def __str__(self):
        return 'Person(name' + self.name + ', public_id=' + self.public_id + ')'


@app.route('/api/v1/admin/user', methods=['POST'])
def create_admin():
    data = request.get_json()
    hased_password = generate_password_hash(
        data['password'], method='sha256')
    public_id = str(uuid.uuid4())
    new_user = User(data['name'], hased_password, public_id, data['admin'])
    # try:
    db.session.add(new_user)
    db.session.commit()
    # except expression as identifier:
    #     print(identifier)

    return jsonify({'message': 'New Admin Added'})


@app.route('/api/v1/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or not data['name'] or not data['password']:
        return make_response('could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required"'})

    user = User.query.filter_by(name=data['name']).first()
    if not user:
        return make_response('could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required"'})

    if check_password_hash(user.password, data['password']):
        token = jwt.encode({'public_id': user.public_id, 'exp': datetime.datetime.utcnow(
        ) + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])
        return jsonify({'token': token.decode('UTF-8')})

    return make_response('could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required"'})

@app.route('/api/v1/get-users', methods=['GET'])
@token_required
def get_all_users(current_user):
    print(current_user)
    if not  current_user.admin:
        return jsonify({'message' : 'You Don\'t have access for this action'})

    users = User.query.all()
    output = []
    for user in users:
        user_data = {}
        user_data['public_id'] = user.public_id
        user_data['name'] = user.name
        user_data['password'] = user.password
        user_data['admin'] = user.admin
        output.append(user_data)
    return jsonify({'users' : output})

if __name__ == "__main__":
    manager.run()
