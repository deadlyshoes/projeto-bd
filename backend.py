from flask import Flask, render_template, url_for, request, redirect

app = Flask(__name__)

	
@app.route("/", methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		if request.form['username'] != "admin" or request.form['password'] != "admin":
			print('Usuário ou senha inválidos.')
		else:
			return redirect(url_for('planetas'))
	return render_template("login.html")

@app.route("/planetas")
def planetas():
	return render_template("planetas.html")

if __name__ == "__main__":
	app.run(debug=True)
