#!/usr/bin/env python3
"""
Task Manager - Created by Genesis AI
"""
from flask import Flask, render_template_string, request, redirect, url_for
import json
from pathlib import Path

app = Flask(__name__)
TASKS_FILE = Path("tasks.json")

def load_tasks():
    if TASKS_FILE.exists():
        with open(TASKS_FILE) as f:
            return json.load(f)
    return []

def save_tasks(tasks):
    with open(TASKS_FILE, "w") as f:
        json.dump(tasks, f, indent=2)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Task Manager</title>
    <style>
        body { font-family: sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; }
        .task { padding: 10px; margin: 5px 0; background: #f0f0f0; border-radius: 5px; }
        .task.done { text-decoration: line-through; color: #888; }
        form { margin: 20px 0; }
        input[type="text"] { padding: 10px; width: 70%; }
        button { padding: 10px 20px; background: #007bff; color: white; border: none; cursor: pointer; }
    </style>
</head>
<body>
    <h1>Task Manager</h1>
    <form method="post">
        <input type="text" name="task" placeholder="Новая задача..." required>
        <button type="submit">Добавить</button>
    </form>
    {% for task in tasks %}
    <div class="task {% if task.done %}done{% endif %}">
        <a href="/toggle/{{ loop.index0 }}">[✓]</a>
        {{ task.text }}
        <a href="/delete/{{ loop.index0 }}" style="color: red;">[✗]</a>
    </div>
    {% endfor %}
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML, tasks=load_tasks())

@app.route("/add", methods=["POST"])
def add():
    tasks = load_tasks()
    tasks.append({"text": request.form["task"], "done": False})
    save_tasks(tasks)
    return redirect(url_for("index"))

@app.route("/toggle/<int:idx>")
def toggle(idx):
    tasks = load_tasks()
    if 0 <= idx < len(tasks):
        tasks[idx]["done"] = not tasks[idx]["done"]
        save_tasks(tasks)
    return redirect(url_for("index"))

@app.route("/delete/<int:idx>")
def delete(idx):
    tasks = load_tasks()
    if 0 <= idx < len(tasks):
        tasks.pop(idx)
        save_tasks(tasks)
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
