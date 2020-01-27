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
		return render_template("entidades.html")	 
	return render_template("login.html")

@app.route("/entidades")
def entidades():
	return render_template("entidades.html")
	
@app.route("/add_planeta", methods=['GET', 'POST'])
def add_planeta():
	if request.method == 'POST':
		nome = request.form["nome"]
		return render_template("entidades.html")	 
	return render_template("add_planeta.html")
	
@app.route("/busca", methods=['GET', 'POST'])
def buscar():
	if request.method == 'POST':
		nome = request.form["nome"]
		return render_template("entidades.html")
	return render_template("busca.html")

if __name__ == "__main__":
	app.run(threaded=True, port=5000)
