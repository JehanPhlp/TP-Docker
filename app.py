# app.py
from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello, World! Depuis Flask dans Docker 🚀"


if __name__ == "__main__":
    # Flask listens on all interfaces inside Docker
    app.run(host="0.0.0.0", port=5000)
