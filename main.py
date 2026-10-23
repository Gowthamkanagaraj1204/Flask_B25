from flask import Flask, render_template,request,redirect

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///user.db'

app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False

db = SQLAlchemy(app)

class Data(db.Model):
    id = db.Column(db.Integer,primary_key =True, autoincrement =True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100),unique =True)

@app.before_request
def create_table():
    db.create_all()

@app.route("/add_user",methods =['GET','POST'])
def home(): 

    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]

        value = Data(name= name,email =email)

        db.session.add(value)
        db.session.commit()

        return"data added"
    
    return render_template("add_user.html")

@app.route("/view_user")
def view():

    value=Data.query.all()
    return render_template("/view_user.html",value = value)



@app.route("/update_user/<int:id>", methods=["GET", "POST"])
def update(id):
    user = Data.query.get_or_404(id)

    if request.method == "POST":
        user.name = request.form["name"]
        user.email = request.form["email"]

        db.session.commit() 

        return "User Updated Successfully"

    return render_template("update_user.html", user = user)
                             
 
@app.route("/delete_user/<int:id>")   
def delete(id):
  
    user=Data.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    # return "User Deleted Successful"
    return redirect("/view_user")

if __name__ == "__main__":
   app.run(debug=True,port=5002) 