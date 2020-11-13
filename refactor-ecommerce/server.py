from src.core.flask_app import app
from src.resource.home import home_blueprint

app.register_blueprint(home_blueprint)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
