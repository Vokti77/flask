from flask import Flask, render_template,request,redirect,url_for # For flask implementation
from bson import ObjectId    # For ObjectId to work
from pymongo import MongoClient
from flask_pymongo import PyMongo
import os

app = Flask(__name__)
cf_port = os.getenv("PORT")

title = "TODO sample application with Flask and MongoDB"
heading = "TODO Reminder with Flask and MongoDB"


app.config['MONGO_URI'] = 'mongodb://localhost:27017/mydata'
mongo = PyMongo(app)
todos_collection = mongo.db.mydata

def redirect_url():
    return request.args.get('next') or \
           request.referrer or \
           url_for('index')


@app.route("/list")
def lists():
    # Display all tasks
    todos_l = todos_collection.find({"done": "no"})
    a1 = "active"
    return render_template('index.html', a1=a1, mongo=todos_l, t=title, h=heading)



@app.route("/")
@app.route("/uncompleted")
def tasks ():
	#Display the Uncompleted Tasks
	todos_l = todos_collection.find({"done":"no"})
	a2="active"
	return render_template('index.html',a2=a2,mongo=todos_l,t=title,h=heading)


@app.route("/completed")
def completed ():
	#Display the Completed Tasks
	todos_l = todos_collection.find({"done":"yes"})
	a3="active"
	return render_template('index.html', a3=a3, mongo=todos_l,t=title,h=heading)

@app.route("/done")
def done ():
	#Done-or-not ICON
	id=request.values.get("_id")
	task=todos_collection.find({"_id":ObjectId(id)})
	if(task[0]["done"]=="yes"):
		todos_collection.update({"_id":ObjectId(id)}, {"$set": {"done":"no"}})
	else:
		todos_collection.update({"_id":ObjectId(id)}, {"$set": {"done":"yes"}})
	redir=redirect_url()	

	return redirect(redir)

@app.route("/action", methods=['POST'])
def action():
    # Adding a Task
    name = request.form.get("name")
    desc = request.form.get("desc")
    date = request.form.get("date")
    pr = request.form.get("pr")
    todos_collection.insert_one({"name": name, "desc": desc, "date": date, "pr": pr, "done": "no"})
    return redirect("/list")


@app.route("/remove")
def remove():
    # Deleting a Task with various references
    task_id = request.args.get("_id")
    todos_collection.delete_one({"_id": ObjectId(task_id)})
    return redirect('/')

@app.route("/update")
def update ():
	id=request.values.get("_id")
	task=todos_collection.find({"_id":ObjectId(id)})
	return render_template('update.html',tasks=task,h=heading,t=title)


@app.route("/action3", methods=['POST'])
def action3():
    # Updating a Task with various references
    name = request.form.get("name")
    desc = request.form.get("desc")
    date = request.form.get("date")
    pr = request.form.get("pr")
    task_id = request.form.get("_id")
    todos_collection.update_one({"_id": ObjectId(task_id)}, {'$set': {"name": name, "desc": desc, "date": date, "pr": pr}})
    return redirect("/")


@app.route("/search", methods=['GET'])
def search():
	#Searching a Task with various references
	key=request.values.get("key")
	refer=request.values.get("refer")
	if(key=="_id"):
		todos_l = todos_collection.find({refer:ObjectId(key)})
	else:
		todos_l = todos_collection.find({refer:key})
	return render_template('searchlist.html',mongo=todos_l,t=title,h=heading)



if __name__ == '__main__':
   if cf_port is None:
       app.run(host='0.0.0.0', port=5000, debug=True)
   else:
       app.run(host='0.0.0.0', port=int(cf_port), debug=True)    
