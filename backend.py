from flask import Flask, jsonify, render_template, url_for, request, redirect

app = Flask(__name__)
	
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

@app.route("/entidades", methods=["GET", "POST"])
def entidades():
	if request.method == "POST":
		nome = request.form["busca"]
		return redirect("entidades")
	return render_template("entidades.html")

@app.route("/adicionar", methods=["GET", "POST"])
def adicionar():
	if request.method == "POST":
		nome = request.form["nome"]
		tipo = request.form["tipo"]
		return redirect("entidades")
	return render_template("adicionar.html")

if __name__ == "__main__":
	app.run(threaded=True, debug=True, port=5000)
