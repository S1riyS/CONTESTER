from flask import Flask

app = Flask(__name__)

# Import routes
with app.app_context():
    from . import routes
