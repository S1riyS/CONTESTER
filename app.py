from app import create_app, db

app = create_app()

if __name__ == "__main__":
    app.run(port=5000, host='127.0.0.1', debug=True)
