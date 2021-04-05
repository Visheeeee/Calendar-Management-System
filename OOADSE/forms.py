from flask_wtf import FlaskForm

from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField

from wtforms.validators import DataRequired, Length, Email, EqualTo





class RegistrationForm(FlaskForm):

    username = StringField('Username',

                           validators=[DataRequired(), Length(min=2, max=20)])


    body = TextAreaField ('Keywords')

    submit = SubmitField('Sign Up')





class LoginForm(FlaskForm):

    email = StringField('Email',

                        validators=[DataRequired(), Email()])

    password = PasswordField('Password', validators=[DataRequired()])

    remember = BooleanField('Remember Me')

    submit = SubmitField('Login')



    