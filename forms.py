from flask_wtf import FlaskForm
from wtforms import TextField, SubmitField, PasswordField, StringField, FileField, MultipleFileField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from wtforms.widgets import TextArea
from flask_wtf.file import FileField


class UserReportForm(FlaskForm):    
    first_name = TextField("First Name",validators=[DataRequired(), Length(min=2, max=50)], render_kw={"placeholder": "ex) Bill"})
    last_name = TextField("Last Name",validators=[DataRequired(), Length(min=2, max=50)], render_kw={"placeholder": "ex) Gates"})
    email = TextField("Email",validators=[DataRequired(),Email()], render_kw={"placeholder": "ex) bill@gmail.com"})
    phone = TextField("Phone",validators=[DataRequired(), Length(min=10, max=15)], render_kw={"placeholder": "ex) 000-000-0000"})
    location = TextField("Location", render_kw={"placeholder": "ex) postal code, street, city, country"})
    plate_number = StringField("Plate Number", render_kw={"placeholder": "AAA001"})
    car_type = StringField("Car Type", render_kw={"placeholder": "Sedan"})
    detail = StringField("Detail", render_kw={"placeholder": ""}, widget=TextArea())
    image = FileField('Image', validators=[])
    video = FileField('Video', validators=[])
    submit = SubmitField("Submit")


class UserRegistrationForm(FlaskForm):
    first_name = TextField("First Name",validators=[DataRequired(), Length(min=1, max=50)], render_kw={"placeholder": "ex) Bill"})
    last_name = TextField("Last Name",validators=[DataRequired(), Length(min=1, max=50)], render_kw={"placeholder": "ex) Gates"})
    email = TextField("Email",validators=[DataRequired(),Email()], render_kw={"placeholder": "ex) bill@gmail.com"})
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6)], render_kw={"placeholder": "ex) password"})
    re_enter_password = PasswordField("Re-Enter password", validators=[DataRequired(), EqualTo('password')], render_kw={"placeholder": "Re-Enter Password"})
    submit = SubmitField("Submit")
    
class UserLoginForm(FlaskForm):
    email = TextField("Email",validators=[DataRequired(),Email()], render_kw={"placeholder": "ex) bill@gmail.com"})
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6)], render_kw={"placeholder": "ex) password"})
    submit = SubmitField("Submit")
    
    
class SearchForm(FlaskForm):
    plate_number = TextField("Plate Number",validators=[], render_kw={""})
    submit1 = SubmitField("Submit")
    
class OperatorReportForm(FlaskForm):
    plate_number = TextField("Plate Number",validators=[], render_kw={""})
    plate_number2 = TextField("Plate Number",validators=[], render_kw={""})
    submit2 = SubmitField("Submit")
