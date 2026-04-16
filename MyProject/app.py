from flask import Flask, render_template, request, redirect, jsonify
import json
import os
from datetime import datetime

app = Flask(__name__)

TODO_FILE = "todo.json"

def load_tasks():
    if not os.path.exists(TODO_FILE):
        return {}
    with open(TODO_FILE, "r") as f:
        return json.load(f)

def save_tasks(tasks):
    with open(TODO_FILE, "w") as f:
        json.dump(tasks, f, indent=4)

@app.route("/")
def home():
    return render_template("index.html")

# Optional API endpoints for server-side task persistence
@app.route("/api/tasks", methods=["GET"])
def get_tasks():
    return jsonify(load_tasks())

@app.route("/api/tasks", methods=["POST"])
def add_task():
    data = request.get_json()
    date_str = data.get("date")
    task_text = data.get("task", "").strip()
    if not date_str or not task_text:
        return jsonify({"error": "Missing date or task"}), 400
    tasks = load_tasks()
    tasks.setdefault(date_str, []).append({"text": task_text, "done": False})
    save_tasks(tasks)
    return jsonify({"success": True, "tasks": tasks.get(date_str, [])})

@app.route("/api/tasks/<date_str>", methods=["PUT"])
def update_tasks(date_str):
    data = request.get_json()
    tasks = load_tasks()
    tasks[date_str] = data.get("tasks", [])
    save_tasks(tasks)
    return jsonify({"success": True})

if __name__ == "__main__":
    app.run(debug=True)