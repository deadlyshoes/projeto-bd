from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'

class LoginForm(FlaskForm):
	username = StringField('Username', validator=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired()])
	submit = SubmitField('Sign In')

@app.route("/")
def index():
	return render_template("inicio.html")
	
@app.route("/login")
def login():
	return render_template("login.html")

if __name__ == "__main__":
	app.run(debug=True)
