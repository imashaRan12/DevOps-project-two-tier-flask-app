from flask import Flask, render_template, request, redirect, url_for, jsonify
import time
import mysql.connector
import os

app = Flask(__name__)

for i in range(10):
    try:
        db = mysql.connector.connect(
            host="mysql",
            user="root",
            password="root",
            database="devops"
        )
        print("Connected to MySQL ✅")
        break
    except Exception as e:
        print("MySQL not ready, retrying...")
        time.sleep(5)
else:
    raise Exception("Could not connect to MySQL")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/dashboard")
def dashboard():
    cursor = db.cursor()

    cursor.execute("SELECT COUNT(*) FROM tasks")
    total = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM tasks WHERE status='done'")
    completed = cursor.fetchone()[0]

    cursor.execute("SELECT * FROM tasks")
    tasks = cursor.fetchall()

    return render_template(
        "dashboard.html",
        tasks=tasks,
        total=total,
        completed=completed
    )

@app.route("/add", methods=["POST"])
def add():

    title = request.form["title"]
    priority = request.form["priority"]
    due = request.form["due"]

    cursor = db.cursor()

    cursor.execute(
        "INSERT INTO tasks(title,priority,due,status) VALUES(%s,%s,%s,'pending')",
        (title,priority,due)
    )

    db.commit()

    return redirect("/dashboard")

@app.route("/complete/<int:id>")
def complete(id):

    cursor = db.cursor()

    cursor.execute(
        "UPDATE tasks SET status='done' WHERE id=%s",(id,)
    )

    db.commit()

    return redirect("/dashboard")

@app.route("/delete/<int:id>")
def delete(id):

    cursor = db.cursor()

    cursor.execute(
        "DELETE FROM tasks WHERE id=%s",(id,)
    )

    db.commit()

    return redirect("/dashboard")

app.run(host="0.0.0.0",port=5000)