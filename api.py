from flask import Flask,request,jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///api.db'
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False

db = SQLAlchemy(app)

class Aathi(db.Model):
    id = db.Column(db.Integer, primary_key =True)
    name = db.Column(db.String(100))

@app.before_request 
def create_table():
    db.create_all()

@app.route("/data",methods = ["POST"])
def add():

    new_data =request.json
    # new_data = Aathi(id = request.json["id"],name =request.json["name"])
    for item in new_data:
        data = Aathi(id = item["id"],name = item["name"])
        db.session.add(data)
    db.session.commit()

    return "data added"

@app.route("/data",methods = ["GET"])
def data():
    view = Aathi.query.all()
    value =[{"id": i.id, "name": i.name} for i in view]
    return jsonify(value)

@app.route("/update/<int:uid>",methods = ["PUT"])
def update(uid):

    update_date = request.json
    item = Aathi.query.get(uid)
    if not item:
        return jsonify ({"message" : "data not found"})
    
    item.name = update_date["name"]
    db.session.commit()

    return jsonify ({"message" : "data updated"})

@app.route("/delete/<int:uid>",methods = ["DELETE"])
def delete(uid):

    item = Aathi.query.get(uid)
    if not item:
        return jsonify ({"message" : "data not found"})
    
    db.session.delete(item)
    db.session.commit()

    return jsonify ({"message" : "data deleted"})

if __name__=="__main__":
    app.run(debug = True, port=5003)

 