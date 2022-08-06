from app import create_app  # lgtm [py/import-own-module]

app = create_app()

if __name__ == "__main__":
    app.run(port=5000, host='127.0.0.1', debug=app.config['DEBUG'])
