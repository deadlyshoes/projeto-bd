from flask import Flask, jsonify, render_template, url_for, request, redirect

app = Flask(__name__)
	
lista = [["0", "Terra", "Planeta", "Sistema Solar", "Via Láctea"], ["1", "Marte", "Planeta", "Sistema Solar", "Via Láctea"]]
lista_info = ["id", "nome", "tipo", "sistema", "galáxia"]
	
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

@app.route("/registro", methods=["GET", "POST"])
def registro():
	if request.method == "POST":
		usuario = request.form["username"]
		senha = request.form["password"]
		return redirect("entidades")
	return render_template("registro.html")

@app.route("/entidades", methods=["GET", "POST"])
def entidades():
	if request.method == "POST":
		nome = request.form["busca"]
		return redirect("entidades")
	return render_template("entidades.html", lista=lista)

@app.route("/entidades/infos/<i>", methods=["GET", "POST"])
def infos(i):
	print(i)
	iden = lista[int(i)]
	return render_template("infos.html", sub=lista[int(i)], inf=lista_info)

@app.route("/adicionar", methods=["GET", "POST"])
def adicionar():
	if request.method == "POST":
		nome = request.form["nome"]
		#tipo = request.form["tipo"]
		return redirect("entidades")
	return render_template("adicionar.html")
	
@app.route("/modificar", methods=["GET", "POST"])
def modificar():
	if request.method == "POST":
		nome = request.form["nome"]
		#tipo = request.form["tipo"]
		return redirect("entidades")
	return render_template("modificar.html")

if __name__ == "__main__":
	app.run(threaded=True, debug=True, port=5000)
