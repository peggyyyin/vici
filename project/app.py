import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session

from werkzeug.security import check_password_hash, generate_password_hash

from functools import wraps

from datetime import datetime, timedelta

#import emoji

app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///vici.db")

def login_required(f):
    # source: adapted from finance problem set
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

#calculate the time you have remaining between the deadline and the present date
def time_left(time_left, time_then, time_now):
    time_then = datetime.strptime(str(time_then), "%Y-%m-%d")
    time_remaining = timedelta(time_left) - (time_now - time_then)
    return (time_remaining.days + 1)

#homepage of tasks, organized by priority
@app.route('/', methods=["GET", "POST"])
@login_required
def home():
    db.execute("CREATE TABLE IF NOT EXISTS tasks (id INTEGER, task TEXT, priority INTEGER, time INTEGER, urgency INTEGER, importance INTEGER, datetime DATETIME)")

    # create table of completed tasks
    completed_task = db.execute("SELECT * FROM tasks WHERE task = ?", request.form.get("delete"))
    completed = []
    for i in completed_task:
        j = {
            "time": i["time"],
            "datetime": i["datetime"]
            }
        completed.append(j)
    
    #create an sql table of completed (conquered) tasks
    if completed_task != []:
        time = completed_task[0]['time']
        time_then = completed_task[0]['datetime']
        time_now = datetime.now()
        db.execute("CREATE TABLE IF NOT EXISTS conquered (id INTEGER, task TEXT, time_remaining INTEGER, datetime DATETIME)")
        db.execute("INSERT INTO conquered (id, task, time_remaining, datetime) VALUES(?, ?, ?, ?)", session["user_id"], completed_task[0]['task'], time_left(time, time_then, time_now), time_now)
        db.execute("DELETE FROM tasks WHERE task = ?", request.form.get("delete"))
    redirect('/')

    #create a prioritized list of tasks to display on the homepage
    priority_list = db.execute("SELECT * FROM tasks WHERE id = ? ORDER BY priority", session["user_id"])
    priorities = []
    for i in priority_list:
        j = {
            "task": i["task"],
            "priority": priority_display(i["priority"]),
            "time": i["time"],
            "urgency": urgent_display(i["urgency"]),
            "importance": importance_display(i["importance"]),
        }
        priorities.append(j)
    return render_template("homepage.html", records=priorities, a=True)

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Query database for username
        db.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER, username TEXT NOT NULL, hash TEXT NOT NULL, PRIMARY KEY (id))")
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return str(400) + " - username not found or password incorrect"

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    session.clear()

    if request.method == "POST":
        db.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER, username TEXT NOT NULL, hash TEXT NOT NULL, PRIMARY KEY (id))")
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Query database for username to make sure it is not taken
        if len(rows) != 0:
            return str(400) + "username already taken"

        else:
            # INSERT the new user into users, storing a hash of the user’s password
            username = request.form.get("username")
            password_hashed = generate_password_hash(request.form.get("password"))
            db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", username, password_hashed)
            return redirect("/")

    else:
        return render_template("register.html")

@app.route("/logout")
def logout():
    """Log user out - source: cs50 finance pset"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

#create more visually-appealing entries for the task log
def urgent_display(urgency):
    if int(urgency) == 100:
        urgent_display = "!!!"
        return urgent_display
    elif int(urgency) == 2:
        urgent_display = "‼️"
        return urgent_display
    elif int(urgency) == 1:
        urgent_display = "!"
        return urgent_display
    else:
        urgent_display = "push"
        return urgent_display

#create more visually-appealing entries for the task log
def importance_display(importance):
    if int(importance) == 100:
        importance_display = ":D"
        return importance_display
    elif int(importance) == 2:
        importance_display = ":)"
        return importance_display
    elif int(importance) == 1:
        importance_display = ":|"
        return importance_display
    else:
        importance_display = "why?"
        return importance_display

#self-made formula to organize tasks in order of perceived priority
def priority(urgency, importance, time):
    return (int(time) * 500) - (100 * int(urgency)) - (10 * int(importance))

#create more visually-appealing entries for the task log
def priority_display(priority_result):
    if priority_result <= 0:
        priority_display = "just do it"
        return priority_display
    elif priority_result <= 380:
        priority_display = "up next"
        return priority_display
    else:
        priority_display = "radar"
        return priority_display

#the dashboard is where users add and delete tasks
@app.route('/dashboard', methods=["GET", "POST"])
@login_required
def dashboard():
    #create task table
    if request.method == "POST":
        task = request.form.get("task")
        urgency = request.form.get("urgency")
        time = request.form.get("time")
        importance = request.form.get("importance")
        db.execute("CREATE TABLE IF NOT EXISTS tasks (id INTEGER, task TEXT, priority INTEGER, time INTEGER, urgency INTEGER, importance INTEGER, datetime DATETIME)")
        
        #gives users an opportunity to delete tasks if they wish
        if task == None:
            db.execute("DELETE FROM tasks WHERE task = ?", request.form.get("delete"))

        #creates task log table
        else:
            db.execute("INSERT INTO tasks (id, task, priority, time, urgency, importance, datetime) VALUES(?, ?, ?, ?, ?, ?, ?)", 
                        session["user_id"], task, priority(urgency, importance, time), time, urgency, importance, datetime.now())
    
    #helps create the table log display
    db.execute("CREATE TABLE IF NOT EXISTS tasks (id INTEGER, task TEXT, priority INTEGER, time datetime, urgency INTEGER, importance INTEGER, datetime DATETIME)")
    task_loop = db.execute("SELECT * FROM tasks WHERE id = ?", session["user_id"])
    record = []
    for i in task_loop:
        j = {
            "task": i["task"],
            "priority": priority_display(i["priority"]),
            "time": i["time"],
            "urgency": urgent_display(i["urgency"]),
            "importance": importance_display(i["importance"]),
        }
        record.append(j)
    return render_template("dashboard.html", records=record, a=True)

#A type of reinforcement schedule (future work)
# def fixed_ratio():
#     completed = db.execute("SELECT tasks FROM conquered where id = ?", session["user_id"])
#     if len(completed) > 0 and len(completed) % 3 == 0:
#         #show the wishlist

#users set their own desired rewards and can view a log of completed tasks
@app.route("/rewards", methods=["GET", "POST"])
@login_required
def rewards():
    #wishlist creation
    if request.method == "POST":
        wish = request.form.get("wish")
        db.execute("CREATE TABLE IF NOT EXISTS rewards (id INTEGER, wish TEXT)")
        if wish == None:
            db.execute("DELETE FROM rewards WHERE wish = ?", request.form.get("delete"))
        else:
            db.execute("INSERT INTO rewards (id, wish) VALUES(?, ?)", session["user_id"], wish)

    #helps create wishlist dropdown menu
    db.execute("CREATE TABLE IF NOT EXISTS rewards (id INTEGER, wish TEXT)")
    wishes = db.execute("SELECT * FROM rewards WHERE id = ?", session["user_id"])
    wishlist = []
    for i in wishes:
        j = {
            "wish": i['wish']
        }
        wishlist.append(j)

    #creates log of completed (conquered) tasks
    db.execute("CREATE TABLE IF NOT EXISTS conquered (id INTEGER, task TEXT, time_remaining INTEGER, datetime DATETIME)")
    conquered = db.execute("SELECT * FROM conquered WHERE id = ?", session["user_id"])
    record = []
    for i in conquered:
        j = {
            "task": i['task'],
            "time_remaining": i['time_remaining'],
            "datetime": i['datetime']
        }
        record.append(j)
    return render_template("rewards.html", records=record, wishlist=wishlist, a=True)