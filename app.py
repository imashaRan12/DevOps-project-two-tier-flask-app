from flask import Flask, render_template, request, redirect, url_for, jsonify
import mysql.connector
import os

app = Flask(__name__)

db = mysql.connector.connect(
    host=os.getenv("MYSQL_HOST"),
    user=os.getenv("MYSQL_USER"),
    password=os.getenv("MYSQL_PASSWORD"),
    database=os.getenv("MYSQL_DB")
)
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