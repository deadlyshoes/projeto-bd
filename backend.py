from flask import Flask, jsonify, render_template, url_for, request, redirect

app = Flask(__name__)

class Usuario():
	def __init__(self, usuario, senha):
		self.usuario = usuario
		self.senha = senha
	
@app.route("/", methods=["GET", "POST"])
def login():
	if request.method == "POST":
		usuario = request.form["username"]
		senha = request.form["password"]
		if (usuario == "deadlyshoes"):
			return render_template("login.html", tipo="error")
		else:
			return redirect("entidades")
	return render_template("login.html", tipo="hidden")

@app.route("/entidades")
def entidades():
	return render_template("entidades.html")

if __name__ == "__main__":
	app.run(threaded=True, debug=True, port=5000)
