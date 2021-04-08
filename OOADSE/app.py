
from flask import Flask, render_template, url_for, flash, redirect
from flask import Flask, request, render_template, send_from_directory
from forms import User, LoginForm,DailyView, WeeklyView, MonthlyView
import jinja2,os
import os
import datetime
import json
import calendar
import threading
from socket import *
from base64 import b64encode, b64decode
import os
from datetime import datetime

      

import sqlite3

conn = sqlite3.connect('database.db')
print("Opened database successfully")


conn.execute('CREATE TABLE IF NOT EXISTS users (name TEXT, email TEXT, password TEXT, UNIQUE(name,email,password) ON CONFLICT IGNORE)') 
print("Table connected successfully")
conn.close()


mail_id=''


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
    form = User(request.form)
    if request.method == 'POST':
        nm=form.username.data
        mail=form.email.data
        pswd=form.password.data
        print(nm)
        with sqlite3.connect("database.db") as con:
            print("inside table")
            cur = con.cursor()
            print('cur created')
            cur.execute("INSERT INTO users (name,email,password) VALUES (?,?,?)",(nm,mail,pswd))
            print('insertion')
            con.commit()
            msg = "Record successfully added"
        file_path='./events/'+mail+'.json'
        f = open(file_path, "w+")
        f.write("[]")
        f.close()
        flash('Thanks for registering','success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

         




@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST':
        mail=form.email.data
        pswd=form.password.data
        with sqlite3.connect("database.db") as  con:
                print("inside table")
                cur = con.cursor()
                cur.execute("SELECT * FROM users WHERE email=? AND password=?", (mail,pswd))
                rows = cur.fetchall()
                if len(rows)>=1: 
                    global mail_id
                    mail_id=mail  
                    print(mail_id)
                    #t1 = threading.Thread(target=send_mail, args=(mail_id,))
                    #t1.start()
                    flash('Successful logged in','success')
                    return render_template("result_login.html",mail=mail,pswd=pswd)
    return render_template('login.html',form=form)





@app.route("/views",methods=['GET','POST'])
def views():
  return render_template("views.html")



@app.route("/dailyviews",methods=['GET','POST'])
def dailyviews():
  day=DailyView()
  c_time=day.current_time
  c_day=day.current_day
  c_month=day.current_month
  c_yr=day.current_year
  c_wkday=day.current_weekday
  global mail_id
  filepath='./events/'+mail_id+'.json'
  day.getevents(filepath)
  c_events=day.events
  print(c_events)
  return render_template('dailyviews.html',day=c_day, month=c_month,year=c_yr,wkday=c_wkday,events=c_events)




@app.route("/weeklyviews",methods=['GET','POST'])
def weeklyviews():
  day=WeeklyView()
  c_time=day.current_time
  c_day=day.current_day
  c_month=day.current_month
  c_yr=day.current_year
  c_wkday=day.current_weekday
  wk_start=day.curr_week_start
  wk_end=day.curr_week_end
  global mail_id
  filepath='./events/'+mail_id+'.json'
  day.getevents(filepath)
  c_events=day.events
  print(c_events)
  return render_template('weeklyviews.html',day=c_day, month=c_month,year=c_yr,wkday=c_wkday,events=c_events,wk_start=wk_start,wk_end=wk_end)




@app.route("/monthlyviews",methods=['GET','POST'])
def monthlyviews():
  day=MonthlyView()
  c_time=day.current_time
  c_day=day.current_day
  c_month=day.current_month
  c_month_num=day.current_month_number
  c_yr=day.current_year
  c_wkday=day.current_weekday
  global mail_id
  filepath='./events/'+mail_id+'.json'
  day.getevents(filepath)
  c_events=day.events
  print(c_events)
  htmlcal = calendar.HTMLCalendar(calendar.MONDAY)
  calendar_code=htmlcal.formatmonth(c_yr,c_month_num)

  return render_template('monthlyviews.html',day=c_day, month=c_month,year=c_yr,wkday=c_wkday,events=c_events,code=calendar_code)






@app.route("/addevent",methods=['GET','POST'])
def addevent():
    return render_template("new_event.html")





@app.route("/deleteevent",methods=['GET','POST'])
def deleteevent():
    return render_template("del_event.html")





@app.route("/event_deleted",methods=['GET','POST'])
def event_deleted():
                eventname = request.form['eventname']
                print(eventname)
                filepath='./events/'+mail_id+'.json'
                f=open(filepath,"r+")
                j=json.loads(f.read())
                f.seek(0)
                f.truncate()
                print(j)
                for i in range(len(j)):
                    if j[i]['title'] == eventname:
                        del j[i]
                        break
                json.dump(j,f)
                return "sucess"





@app.route("/event_added",methods=['GET','POST'])
def event_added():
                eventname = request.form['eventname']
                startdate = request.form['startdate']
                enddate = request.form['enddate']
                option = request.form['reminder']
                print(option)
                res={}
                res['title']=eventname
                res['start']=startdate
                res['end']=enddate
                res['reminder']=option
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






def send_mail(mail_id):
  # print('mail func started')
  while(True):

    f = open('./events/' + mail_id + '.json', 'r+')
    j = json.loads(f.read())

    for i in range(len(j)):
      if j[i]['reminder'] == 'yes':
        # print('entered if yes')
        now = datetime.now()
        startdate = list(map(int, j[i]['start'].split('-')))

        startevent = datetime(startdate[0], startdate[1], startdate[2])
        print(startevent - now)
        print((startevent - now).days)
        if((startevent-now).days <= 1):
          print('-----------Email ready to send--------')
          j[i]['reminder'] = 'no'

          endmsg = '\r\n.\r\n'

          # Sender - email, password and Receiver - email DETAILS
          sender_email = 'navaneethmukund.nm@gmail.com'
          sender_password = 'navaneeth123'
          receiver_email = mail_id
          # Encoding sender email and password in base64 format
          encoded_sender_email = b64encode(sender_email.encode('ascii'))
          encoded_sender_password = b64encode(sender_password.encode('ascii'))

          # Choose a mail server (e.g. Google mail server) and call it mailserver
          mailserver = 'smtp.gmail.com'

          # Create socket called clientSocket
          clientSocket = socket(AF_INET, SOCK_STREAM)

          # Establish a TCP connection with mailserver (Port number may change according to the mail server)
          clientSocket.connect((mailserver, 587))
          recv = clientSocket.recv(1024).decode()
          print (recv)
          if recv[:3] != '220':
            print('220 reply not received from server.')

          # Send HELO command and print server response.
          heloCommand = 'HELO google\r\n'
          clientSocket.send(heloCommand.encode())
          recv1 = clientSocket.recv(1024).decode()
          print (recv1)
          if recv1[:3] != '250':
            print('250 reply not received from server.')

          # STARTTLS
          startTls = 'starttls auth login\r\n'
          clientSocket.send(startTls.encode())
          recv2 = clientSocket.recv(1024).decode()
          print (recv2)
          if recv2[:3] != '555':
            print('555 reply not received from server.')

          # Auth login
          authLogin = 'auth login\r\n'
          clientSocket.send(authLogin.encode())

          # This is a base64 encoded string asking for username
          recv3 = clientSocket.recv(1024)
          if recv3.decode()[:3] != '334':
            print('334 reply not received from server.')
          print(recv3.decode().strip() + ' => gmail asking for ' + b64decode(recv3.split()[1]).decode('ascii')[:-1] + '\n')
          # Sending sender_email
          clientSocket.send(encoded_sender_email + '\r\n'.encode())

          # This is a base64 encoded string asking for password
          recv4 = clientSocket.recv(1024)
          if recv4.decode()[:3] != '334':
            print('334 reply not received from server.')
          print(recv4.decode().strip() + ' => gmail asking for ' + b64decode(recv4.split()[1]).decode('ascii')[:-1] + '\n')
          # Sending sender_password
          clientSocket.send(encoded_sender_password + '\r\n'.encode())

          # Looking for 235 Accepted response
          recv5 = clientSocket.recv(1024).decode()
          print (recv5)
          if recv5[:3] != '235':
            print('235 reply not received from server. Probably Auth login unsuccessful')

          # Send MAIL FROM command and print server response.
          mailfrom = 'MAIL FROM: <' + sender_email + '>\r\n'
          clientSocket.send(mailfrom.encode())
          recv6 = clientSocket.recv(1024).decode()
          print (recv6)
          if recv6[:3] != '250':
            print('250 reply not received from server.')

          # Send RCPT TO command and print server response. 
          rcptto = 'RCPT TO: <' + receiver_email + '>\r\n'
          clientSocket.send(rcptto.encode())
          recv7 = clientSocket.recv(1024).decode()
          print (recv7)
          if recv7[:3] != '250':
            print('250 reply not received from server.')

          # Send DATA command and print server response. 
          data = 'DATA\r\n'
          clientSocket.send(data.encode())
          recv8 = clientSocket.recv(1024).decode()
          print (recv8)
          if recv8[:3] != '354':
            print('354 reply not received from server.')

          # Send message data.
          clientSocket.send('SUBJECT: Event Remainder!\r\n'.encode())
          email_msg = j[i]['title'] + ' is scheduled tomorrow'
          clientSocket.send(email_msg.encode())

          # Message ends with a single period.
          clientSocket.send(endmsg.encode())
          recv9 = clientSocket.recv(1024).decode()
          print (recv9)
          if recv9[:3] != '250':
            print('250 reply not received from server.')

          # Send QUIT command and get server response.
          quitcommand = 'QUIT\r\n'
          clientSocket.send(quitcommand.encode())
          recv10 = clientSocket.recv(1024).decode()
          print (recv10)
          if recv10[:3] != '221':
            print('221 reply not received from server.')

          # Closing TCP Connection
          clientSocket.close()
    f.seek(0)
    f.truncate()
    json.dump(j, f)
    f.close()





if __name__ == '__main__':

    app.run(host="localhost", port=5000, debug=True)
