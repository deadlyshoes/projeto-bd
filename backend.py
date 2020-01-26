from flask import Flask, render_template, url_for, request, redirect

app = Flask(__name__)

class Usuario():
	def __init__(self, usuario, senha):
		self.usuario = usuario
		self.senha = senha
	
	
@app.route("/", methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		usuario = request.form["username"]
		senha = request.form["password"]
		return render_template("planetas.html")	 
	return render_template("login.html")

@app.route("/registrar", methods=['GET', 'POST'])
def registro():
	if request.method == 'POST':
		usuario = request.form["username"]
		senha = request.form["password"]
		return render_template("planetas.html")
	return render_template("registro.html")

@app.route("/planetas")
def planetas():
	return render_template("planetas.html")

if __name__ == "__main__":
	app.run(debug=True)
