from app import app

if __name__ == "__main__":
    app.secret_key = "Hello World"
    app.run(debug=True)
