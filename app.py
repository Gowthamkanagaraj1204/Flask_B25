from flask import Flask,render_template,request
import sqlite3

conn = sqlite3.connect("newdata.db",check_same_thread= False)

app = Flask(__name__)

cur = conn.cursor()

cur.execute("""CREATE TABLE IF NOT EXISTS TAB(
id INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT NOT NULL,
password TEXT NOT NULL)""")

conn.commit()

@app.route("/signup",methods = ['GET','POST'])
def signup():

    if request.method == 'POST':
        name =request.form['name']
        psw = request.form['password']
        cur.execute("INSERT INTO TAB(name,password) VALUES(?,?)",(name,psw))

        conn.commit()

    return render_template("signup.html")

if __name__=="__main__": 
    app.run(debug = True)