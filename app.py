from app import app  # lgtm [py/import-own-module]

if __name__ == "__main__":
    app.run(port=5000, host='127.0.0.1', debug=True)
