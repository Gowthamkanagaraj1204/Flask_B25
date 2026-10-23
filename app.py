from flask import Flask,render_template,request,redirect
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

@app.route("/view")
def view():
    cur.execute("SELECT * FROM TAB")

    gt = cur.fetchall()

    return render_template("view.html",get = gt)



@app.route("/update/<id>", methods=['GET', 'POST'])
def update(id):

    if request.method == "POST":
        new_name = request.form["name"]
        new_psw = request.form["password"]

        cur.execute("UPDATE TAB SET name = ?,password = ? WHERE id = ?",
            (new_name, new_psw, id))
        conn.commit()

        return redirect("/view")

    cur.execute("SELECT * FROM TAB WHERE id = ?", (id,))
    user = cur.fetchone()

    return render_template("update.html", user=user)
 
@app.route("/delete/<id>")
def delete(id):
       
    cur.execute("DELETE FROM TAB WHERE id = ?",(id,))

    conn.commit()

    return redirect("/view")
 

if __name__=="__main__":
    app.run(debug = True,port=5002)