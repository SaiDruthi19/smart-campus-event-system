from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Database connection
def get_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn


# Home page - show events
@app.route("/")
def index():
    conn = get_db()
    events = conn.execute("SELECT * FROM events").fetchall()
    return render_template("index.html", events=events)


# Admin dashboard
@app.route("/admin")
def admin():

    conn = get_db()

    events = conn.execute("SELECT * FROM events").fetchall()

    count = conn.execute("SELECT COUNT(*) FROM events").fetchone()[0]

    return render_template("admin.html", events=events, count=count)


# Add event
@app.route("/add_event", methods=["POST"])
def add_event():

    name = request.form["name"]
    date = request.form["date"]
    description = request.form["description"]

    conn = get_db()

    conn.execute(
        "INSERT INTO events(event_name, event_date, event_description) VALUES (?,?,?)",
        (name, date, description)
    )

    conn.commit()

    return redirect("/admin")


# Delete event
@app.route("/delete_event/<int:event_id>")
def delete_event(event_id):

    conn = get_db()

    conn.execute("DELETE FROM events WHERE id = ?", (event_id,))

    conn.commit()

    return redirect("/admin")


# Register for event
@app.route("/register/<int:event_id>", methods=["GET", "POST"])
def register(event_id):

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        branch = request.form["branch"]

        conn = get_db()

        conn.execute(
            "INSERT INTO users(name,email,branch) VALUES (?,?,?)",
            (name, email, branch)
        )

        user_id = conn.execute(
            "SELECT last_insert_rowid()"
        ).fetchone()[0]

        conn.execute(
            "INSERT INTO registrations(user_id,event_id) VALUES (?,?)",
            (user_id, event_id)
        )

        conn.commit()

        return redirect("/")

    return render_template("register.html")


# View participants
@app.route("/participants/<int:event_id>")
def participants(event_id):

    conn = get_db()

    data = conn.execute("""
        SELECT users.name, users.email, users.branch
        FROM users
        JOIN registrations
        ON users.id = registrations.user_id
        WHERE registrations.event_id = ?
    """, (event_id,)).fetchall()

    return render_template("participants.html", data=data)


# Analytics page
@app.route("/analytics")
def analytics():

    conn = get_db()

    data = conn.execute("""
        SELECT events.event_name, COUNT(registrations.id) as total
        FROM events
        LEFT JOIN registrations
        ON events.id = registrations.event_id
        GROUP BY events.id
    """).fetchall()

    return render_template("analytics.html", data=data)


# Run server
if __name__ == "__main__":
    app.run(debug=True)