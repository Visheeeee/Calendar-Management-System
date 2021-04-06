
from flask import Flask, render_template, url_for, flash, redirect
from flask import Flask, request, render_template, send_from_directory
from forms import RegistrationForm, LoginForm
import jinja2,os
import os
import datetime
import json
import calendar

import sqlite3

conn = sqlite3.connect('database.db')
print("Opened database successfully")


conn.execute('CREATE TABLE IF NOT EXISTS users (name TEXT, email TEXT, password TEXT)')
print("Table connected successfully")
conn.close()


mail_id='v@gmail.com'


app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
APP_ROOT = os.path.dirname(os.path.abspath("__file__"))



@app.route("/")

@app.route("/home")
def home():
    flash('Welcome to Calender', 'success')
    return render_template('home.html')





@app.route("/about")

def about():

    return render_template('about.html', title='About')








@app.route("/register", methods=["POST","GET"])
def register():
    return render_template('default1.html')






@app.route("/signedup",methods=["POST","GET"])
def signedup():
  
   if request.method == 'POST':
      try:
         nm = request.form['fname']
         mail = request.form['email']
         pswd = request.form['password']
         print(nm,mail,pswd)
         
         with sqlite3.connect("database.db") as con:
            print("inside table")
            cur = con.cursor()
            print('cur created')
            cur.execute("INSERT INTO users (name,email,password) VALUES (?,?,?)",(nm,mail,pswd))
            print('insertion')
            con.commit()
            msg = "Record successfully added"
      except:
         con.rollback()
         msg = "error in insert operation"
      
      finally:
         con.close() 
         file_path='./events/'+mail+'.json'
         f = open(file_path, "w+")
         f.write("[]")
         f.close()
            
         return render_template("result.html")
         






@app.route("/loggedup",methods=["POST","GET"])
def loggedup():
  
    if request.method == 'POST':
        try:
            mail = request.form['email']
            pswd = request.form['password']
            print(mail,pswd)

            with sqlite3.connect("database.db") as  con:
                print("inside table")
                cur = con.cursor()
                cur.execute("SELECT * FROM users WHERE email=? AND password=?", (mail,pswd))
                rows = cur.fetchall()
                if len(rows)>=1:
                    global mail_id 
                    mail_id=mail
                    return render_template("result_login.html",mail=mail,pswd=pswd)

        except:
             
             msg = "error in insert operation"
      
        finally:
             con.close()




@app.route("/views",methods=['GET','POST'])
def views():
    return render_template("json.html")






@app.route("/addevent",methods=['GET','POST'])
def addevent():
    return render_template("new_event.html")







@app.route("/event_added",methods=['GET','POST'])
def event_added():
                eventname = request.form['eventname']
                startdate = request.form['startdate']
                enddate = request.form['enddate']
                res={}
                res['title']=eventname
                res['start']=startdate
                res['end']=enddate
                filepath='./events/'+mail_id+'.json'
                f=open(filepath,"r+")
                j=json.loads(f.read())
                f.seek(0)
                f.truncate()
                j.append(res)
                print(j)
                json.dump(j,f)
                
                return "sucess"






















@app.route('/data')
def return_data():
    start_date = request.args.get('start', '')
    end_date = request.args.get('end', '')
    # You'd normally use the variables above to limit the data returned
    # you don't want to return ALL events like in this code
    # but since no db or any real storage is implemented I'm just
    # returning data from a text file that contains json elements
    filepath='./events/'+mail_id+'.json'
    print(mail_id)
    with open(filepath, "r") as input_data:
        # you should use something else here than just plaintext
        # check out jsonfiy method or the built in json module
        # http://flask.pocoo.org/docs/0.10/api/#module-flask.json
        
        return input_data.read()






@app.route("/login", methods=['GET', 'POST'])

def login():

    return render_template('login.html')



if __name__ == '__main__':

    app.run(host="0.0.0.0", port=5000, debug=True)
