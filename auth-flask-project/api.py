from flask import Flask, request, jsonify, make_response
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import uuid

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/apiAuth'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

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


if __name__ == "__main__":
    manager.run()
