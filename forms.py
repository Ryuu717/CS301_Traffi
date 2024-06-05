from flask_wtf import FlaskForm
from wtforms import TextField, SubmitField, PasswordField, StringField, FileField, MultipleFileField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from wtforms.widgets import TextArea

import datetime


class UserReportForm(FlaskForm):    
    first_name = TextField("First Name",validators=[DataRequired(), Length(min=2, max=50)], render_kw={"placeholder": "ex) John"})
    last_name = TextField("Last Name",validators=[DataRequired(), Length(min=2, max=50)], render_kw={"placeholder": "ex) Wick"})
    email = TextField("Email",validators=[DataRequired(),Email()], render_kw={"placeholder": "ex) abc@gmail.com"})
    phone = TextField("Phone",validators=[DataRequired(), Length(min=10, max=15)], render_kw={"placeholder": "ex) 012-3456-7890"})
    location = TextField("Location", render_kw={"placeholder": "ex) postal code, street, city, country"})
    detail = StringField("Detail", render_kw={"placeholder": ""}, widget=TextArea())
    # image = FileField("Image")
    # video = FileField("Video")
    files = MultipleFileField(render_kw={'multiple': True})
    # card_number = TextField("Card Number", render_kw={"placeholder": "ex) 0000-0000-0000"})
    # password = PasswordField("Password", validators=[DataRequired(), Length(min=6)], render_kw={"placeholder": "ex) abc123"})
    # re_enter_password = PasswordField("Re-Enter password", validators=[DataRequired(), EqualTo('password')], render_kw={"placeholder": "Re-Enter Password"})
    submit = SubmitField("Submit")


class UserRegistrationForm(FlaskForm):
    first_name = TextField("First Name",validators=[DataRequired(), Length(min=2, max=50)], render_kw={"placeholder": "ex) John"})
    last_name = TextField("Last Name",validators=[DataRequired(), Length(min=2, max=50)], render_kw={"placeholder": "ex) Wick"})
    email = TextField("Email",validators=[DataRequired(),Email()], render_kw={"placeholder": "ex) abc@gmail.com"})
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6)], render_kw={"placeholder": "ex) abc123"})
    re_enter_password = PasswordField("Re-Enter password", validators=[DataRequired(), EqualTo('password')], render_kw={"placeholder": "Re-Enter Password"})
    # image = FileField("Image")
    # video = FileField("Video")
    # files = MultipleFileField(render_kw={'multiple': True})
    # card_number = TextField("Card Number", render_kw={"placeholder": "ex) 0000-0000-0000"})
    # password = PasswordField("Password", validators=[DataRequired(), Length(min=6)], render_kw={"placeholder": "ex) abc123"})
    # re_enter_password = PasswordField("Re-Enter password", validators=[DataRequired(), EqualTo('password')], render_kw={"placeholder": "Re-Enter Password"})
    submit = SubmitField("Submit")
    
class UserLoginForm(FlaskForm):
    email = TextField("Email",validators=[DataRequired(),Email()], render_kw={"placeholder": "ex) abc@gmail.com"})
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6)], render_kw={"placeholder": "ex) abc123"})
    submit = SubmitField("Submit")
    
# class RegisterGuestForm(FlaskForm):
#     first_name = TextField("First Name",validators=[DataRequired(), Length(min=2, max=50)], render_kw={"placeholder": "ex) John"})
#     last_name = TextField("Last Name",validators=[DataRequired(), Length(min=2, max=50)], render_kw={"placeholder": "ex) Wick"})
#     address = TextField("Address", validators=[DataRequired()], render_kw={"placeholder": "ex) postal code, street, city, country"})
#     phone = TextField("Phone",validators=[DataRequired(), Length(min=10, max=15)], render_kw={"placeholder": "ex) 012-3456-7890"})
#     email = TextField("Email",validators=[DataRequired(),Email()], render_kw={"placeholder": "ex) abc@gmail.com"})
#     card_number = TextField("Card Number",validators=[DataRequired()], render_kw={"placeholder": "ex) 0000-0000-0000"})
#     submit = SubmitField("Submit")

# class RegisteredForm(FlaskForm):
#     first_name = TextField("First Name",validators=[DataRequired(), Length(min=2, max=50)])
#     last_name = TextField("Last Name",validators=[DataRequired(), Length(min=2, max=50)])
#     address = TextField("Address",validators=[DataRequired()])
#     phone = TextField("Phone",validators=[DataRequired(), Length(min=10, max=15)])
#     email = TextField("Email",validators=[DataRequired(),Email()])
#     card_number = TextField("Card Number",validators=[DataRequired()])
