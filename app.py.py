from flask import Flask, request
import os
import pickle

app = Flask(__name__)

# Hardcoded secret key
app.config['SECRET_KEY'] = "supersecret123"


@app.route("/")
def index():
    return "Welcome to vulnerable app!"


# SQL Injection
@app.route("/login")
def login():
    username = request.args.get("user")
    query = "SELECT * FROM users WHERE name = '" + username + "'"
    # Імітація виконання SQL-запиту
    return f"Executing query: {query}"


# Command Injection
@app.route("/run")
def run_command():
    cmd = request.args.get("cmd")
    return os.popen(cmd).read()


# Insecure deserialization
@app.route("/load", methods=["POST"])
def load_data():
    data = request.data
    return pickle.loads(data)  # Небезпечно


# Path Traversal
@app.route("/file")
def read_file():
    filename = request.args.get("name")
    with open("/tmp/" + filename) as f:
        return f.read()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
