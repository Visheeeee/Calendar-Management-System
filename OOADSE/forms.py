from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, RadioField, DateField
from wtforms import Form, BooleanField, StringField, PasswordField, validators
from wtforms.validators import DataRequired, Length, Email, EqualTo
import json
from datetime import datetime,date, timedelta
import calendar
import sqlite3

class User(FlaskForm):

    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email Address', [validators.Length(min=6, max=35)])
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')

    def register(self):
        with sqlite3.connect("database.db") as con:
            print("inside table")
            cur = con.cursor()
            print('cur created')
            cur.execute("INSERT INTO users (name,email,password) VALUES (?,?,?)",(self.username.data, self.email.data, self.password.data))
            print('insertion')
            con.commit()
            msg = "Record successfully added"
        file_path='./events/'+self.email.data+'.json'
        f = open(file_path, "w+")
        f.write("[]")
        f.close()






class LoginForm(FlaskForm):

    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])


    def login(self):
        mail=self.email.data
        pswd=self.password.data
        with sqlite3.connect("database.db") as  con:
                print("inside table")
                cur = con.cursor()
                cur.execute("SELECT * FROM users WHERE email=? AND password=?", (mail,pswd))
                rows = cur.fetchall()
                if len(rows)>=1:
                    return True
        return False




class DailyView(FlaskForm):

   
    current_time = datetime.now()
    current_day=current_time.date()
    current_month=current_time.strftime("%B")
    current_year=current_time.year
    current_weekday=current_time.strftime("%A")
    events=[]

    

    def getevents(self, filepath):
        f=open(filepath,"r")
        j=json.loads(f.read())
        for i in range(len(j)):
            startdate = list(map(int, j[i]['start'].split('-')))
            startevent = date(startdate[0], startdate[1], startdate[2])
            print(startevent,self.current_day)
            if startevent == self.current_day and j[i]['title'] not in self.events: 
                self.events.append(j[i]['title'])
        f.close()




class WeeklyView(FlaskForm):

   
    current_time = datetime.now()
    current_day=current_time.date()
    current_month=current_time.strftime("%B")
    current_year=current_time.year
    current_weekday=current_time.strftime("%A")
    current_week_number=current_time.strftime("%V")
    events=[]
    curr_week_start=current_day - timedelta(days=current_day.weekday())
    curr_week_end=curr_week_start + timedelta(days=6)    


    def getevents(self, filepath):
        f=open(filepath,"r")
        j=json.loads(f.read())
        for i in range(len(j)):
            startdate = list(map(int, j[i]['start'].split('-')))
            startevent = date(startdate[0], startdate[1], startdate[2])
            start = self.current_day - timedelta(days=self.current_day.weekday())
            end = start + timedelta(days=6)
            if startevent>=start and startevent<=end:
                this_list=[j[i]['title'],j[i]['start']]
                if this_list not in self.events:
	                self.events.append([j[i]['title'],j[i]['start']])
        f.close()   

    


class MonthlyView(FlaskForm):

   
    current_time = datetime.now()
    current_day=current_time.date()
    current_month=current_time.strftime("%B")
    current_month_number=current_time.month
    current_year=current_time.year
    current_weekday=current_time.strftime("%A")
    current_week_number=current_time.strftime("%V")
    events=[]

    


    def getevents(self, filepath):
        f=open(filepath,"r")
        # print(f.read())
        j=json.loads(f.read())
        print(j)
        self.events=[]
        for i in range(len(j)):
            startdate = list(map(int, j[i]['start'].split('-')))
            startevent = date(startdate[0], startdate[1], startdate[2])
            first_day = self.current_day.replace(day = 1)
            next_month = self.current_day.replace(day=28) + timedelta(days=4)
            last_day=next_month - timedelta(days=next_month.day)

            if startevent>=first_day and startevent<=last_day:
                this_list=[j[i]['title'],j[i]['start']]
                if this_list not in self.events:
	                self.events.append([j[i]['title'],j[i]['start']])
        f.flush()
        f.close()

        




class Event(FlaskForm):
    eventname = StringField('Eventname', validators=[DataRequired(), Length(min=2, max=20)])
    startdate = StringField('Startdate', validators=[DataRequired(), Length(min=2, max=20)])
    enddate = StringField('Enddate', validators=[DataRequired(), Length(min=2, max=20)])
    option = RadioField('option', choices = ['yes', 'no'])

    def has_reminder(self):
        if self.option.data == 'yes':
            return True
        return False

    def add_event(self, mail_id):
        eventname = self.eventname.data
        startdate = self.startdate.data
        enddate = self.enddate.data
        option = self.option.data
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
        f.flush()
        f.close()

    
    def deleteevent(self,mail_id):
        eventname = self.eventname.data
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
        f.flush()
        f.close()
       

