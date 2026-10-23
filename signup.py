from flask import Flask, render_template,request,session,redirect
import sqlite3

app = Flask(__name__)
app.secret_key = "hlo123"

conn = sqlite3.connect("newdata.db", check_same_thread=False)

cur = conn.cursor()

cur.execute("""
 
CREATE TABLE IF NOT EXISTS STUDENTS (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    password TEXT NOT NULL,
    email VARCHAR(30)
)
""")

conn.commit()


# SIGNUP
@app.route("/signup", methods=["GET", "POST"])
def signup():

    if request.method == "POST":
        name = request.form["username"]
        email = request.form["email"]
        psw = request.form["password"]

        cur.execute(
            "INSERT INTO STUDENTS (username, email, password) VALUES (?, ?, ?)",
            (name, email, psw)
        )
        conn.commit()

        return redirect("/login")

    return render_template("newsignup.html")


# LOGIN
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":
        name = request.form["name"]
        psw = request.form["password"]

        cur.execute(
            "SELECT * FROM STUDENTS WHERE username = ?",
            (name,)
        )

        details = cur.fetchone()

        if details and details[1] == name and str(details[2]) == psw:
            session["name"] = name

            # Login successful: redirect to home page
            return redirect("/smpt")

        else:
            # Invalid username or password: stay on login page
            return render_template(
                "newlogin.html",
                error="Invalid username or password!"
            )

    return render_template("newlogin.html")

@app.route("/smpt", methods=["GET", "POST"])
def smpt():

    if request.method == "POST":
        senderemail = request.form["sender_email"]
        toemail = request.form["to_email"]

        return render_template("smpt.html")

    return redirect("/home")


# HOME
@app.route("/home")
def home():

    if "name" in session:
        return render_template("home.html", name=session["name"])

    return redirect("/login")


# LOGOUT
@app.route("/logout")
def logout():

    session.clear()

    return redirect("/login")


if __name__ == "__main__":
    app.run(debug=True, port=5003)