from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms import Form, BooleanField, StringField, PasswordField, validators
from wtforms.validators import DataRequired, Length, Email, EqualTo
import json
from datetime import datetime,date, timedelta
import calendar


class User(FlaskForm):

    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email Address', [validators.Length(min=6, max=35)])
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')

    





class LoginForm(FlaskForm):

    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])








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
        j=json.loads(f.read())
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


        


