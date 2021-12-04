from flask import Flask

app = Flask(__name__)

# Jinja2 global variables
variables = {
    'WEBSITE_URL': 'сontester17.herokuapp.com',
    'LANGUAGE': 'ru',
    'DEVELOPER': 'S1riyS'
}
for key, value in variables.items():
    app.jinja_env.globals[key] = value

# Import routes
with app.app_context():
    from web import routes
