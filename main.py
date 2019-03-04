from flask import Flask,render_template,request,redirect,url_for,flash,session
import pygal
from flask_sqlalchemy import SQLAlchemy

DB_URL = 'postgresql://postgres:12031994@127.0.0.1:5432/projectManagementSystem'

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']= DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False
app.config['SECRET_KEY'] ='some-string'

db = SQLAlchemy(app)

from models import ProjectModel
from userModel import Authentication

@app.before_first_request
def createTables():
    db.create_all()


@app.route('/authentication', methods=['GET'])
def authentication():
    return render_template("authentication.html")


@app.route('/', methods=['GET'])
def home():
    if session:
        return render_template("index.html")
     #   if session is set
    else:
#         if session is not set
@app.route()
@app.route('/register',methods=['POST'])
def addNewUser():
    fullName = request.form['fullName']
    email = request.form['email']
    password = request.form['password']
    confirmpw = request.form['confirmPassword']
    # check if password and confirm password match
    if password != confirmpw:
        flash("Password don't match")
        return render_template('authentication.html')

    elif (Authentication.check_mail(email)):
        flash("User already exists")
        return render_template('authentication.html')
    else:
    # create user
        register= Authentication(fullName=fullName, email=email,password=password)
        register.createUser()
        flash("You have been registered")
    # create session
    session['email']=email
    # session['fullName']=fullName
        return redirect(url_for('home'))
        return render_template("index.html")

#task-make a graph that includes cost
@app.route('/project/create',methods=['POST'])
def addNewProject():
    if request.method=='POST':
        title = request.form['title']
        description = request.form['description']
        startDate = request.form['startDate']
        endDate =request.form['endDate']
        cost= request.form['cost']
        status = request.form['status']
        project= ProjectModel(title=title, description=description,startDate=startDate,endDate=endDate,cost=cost,status=status)
        project.create_Record()
        return redirect(url_for('home'))

@app.route('/project/edit/<int:id>',methods=['POST'])
def edditProject(id):
    newTitle = request.form['title']
    newDescription = request.form['description']
    newStartDate = request.form['startDate']
    newEndDate = request.form['endDate']
    newCost = request.form['cost']
    newStatus= request.form['status']
    updated = ProjectModel.update_by_id(id=id,newTitle=newTitle,newDescription=newDescription,newStartDate=newStartDate,newEndDate=newEndDate,newCost=newCost,newStatus=newStatus)

    if updated:
        flash("Updated Successfully")
        return redirect(url_for('home'))

    else:
        flash("No Record Found")
        return redirect(url_for("home"))
@app.route('/project/delete/<int:id>',methods=['POST'])
def deleteRecord(id):
    deleted= ProjectModel.delete_by_id(id)
    if deleted:
        flash("Deleted Successfully")
        return redirect(url_for('home'))#
    else:
        flash("Recoed Not Deleted")
        return redirect(url_for('home'))





if __name__ == "__main__":
    app.run(port=5000,debug=True)
