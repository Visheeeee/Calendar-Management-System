
from flask import Flask, render_template, url_for, flash, redirect
from flask import Flask, request, render_template, send_from_directory
from forms import User, LoginForm,DailyView, WeeklyView, MonthlyView, Event
import jinja2,os
import os
import datetime
import json
import calendar
import threading
from socket import *
from base64 import b64encode, b64decode
import os
from datetime import datetime, date, timedelta

      

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
    flash('Welcome to Calendar', 'success')
    return render_template('home.html')





@app.route("/about")

def about():

    return render_template('about.html', title='About')








@app.route("/register", methods=["POST","GET"])
def register():
    user = User(request.form)
    if request.method == 'POST':
        user.register()
        flash('Thanks for registering','success')
        return redirect(url_for('login'))
    return render_template('register.html', form=user)

         




@app.route("/login", methods=['GET', 'POST'])
def login():
    user = LoginForm(request.form)
    if request.method == 'POST':
        if(user.login()): 
            global mail_id
            mail_id=user.email.data  
            print(mail_id)
            t1 = threading.Thread(target=send_mail, args=(mail_id,))
            t1.start()
            flash('Successful logged in','success')
            return render_template("result_login.html",mail=user.email.data,pswd=user.password.data)
    return render_template('login.html',form=user)





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
  filepath='./users/'+mail_id+'.json'
  day.getevents(filepath)
  c_events=day.events
  print(c_events)
  return render_template('dailyviews.html',day=c_day, month=c_month,year=c_yr,wkday=c_wkday,events=c_events)


prev_day_count = 0
@app.route("/prevdayview", methods=['GET, POST'])
def get_prev_day():
  if request.method == "POST":
    prev_day_count += 1
    day=DailyView()
    p_day=day.current_day - timedelta(prev_day_count)
    day.current_day = p_day
    p_month=p_day.strftime("%B")
    day.current_month = p_month
    p_yr=p_day.year
    day.current_year = p_yr
    p_wkday=p_day.strftime("%A")
    day.current_weekday = p_wkday
    global mail_id
    filepath='./users/'+mail_id+'.json'
    day.getevents(filepath)
    p_events=day.events
    print(p_events)
    return render_template('dailyviews.html',day=p_day, month=p_month,year=p_yr,wkday=p_wkday,events=p_events)






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
  filepath='./users/'+mail_id+'.json'
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
  filepath='./users/'+mail_id+'.json'
  day.getevents(filepath)
  c_events=day.events
  print(c_events)
  htmlcal = calendar.HTMLCalendar(calendar.MONDAY)
  calendar_code=htmlcal.formatmonth(c_yr,c_month_num)
  del day
  return render_template('monthlyviews.html',day=c_day, month=c_month,year=c_yr,wkday=c_wkday,events=c_events,code=calendar_code)






@app.route("/addevent",methods=['GET','POST'])
def addevent():
    event = Event(request.form)
    if request.method == 'POST':
      global mail_id
      event.add_event(mail_id)      
      # return "sucess" # render a html file later
      flash('Event Added','success')
      return render_template("result_login.html",mail=mail_id)
    return render_template("new_event.html", form=event)





@app.route("/deleteevent",methods=['GET','POST'])
def deleteevent():
    event = Event(request.form)
    if request.method == 'POST':
      global mail_id
      event.deleteevent(mail_id)
      flash('Event Deleted','success')
      return render_template("result_login.html",mail=mail_id)
    return render_template("del_event.html",form=event)




def send_mail(mail_id):
  # print('mail func started')
  while(1):


    f = open('./users/' + mail_id + '.json', 'r+')
    j = json.loads(f.read())

    for i in range(len(j)):
      if j[i]['reminder'] == 'yes':
        # print('entered if yes')
        now = datetime.now().date()
        startdate = list(map(int, j[i]['start'].split('-')))

        startevent = date(startdate[0], startdate[1], startdate[2])
        print(startevent - now)
        print((startevent - now).days)
        if((startevent-now).days == 1):
          print('-----------Email ready to send--------')
          j[i]['reminder'] = 'no'

          endmsg = '\r\n.\r\n'

          # Sender - email, password and Receiver - email DETAILS
          sender_email = ''
          sender_password = ''
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
          clientSocket.send('SUBJECT: Event Reminder!\r\n'.encode())
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
