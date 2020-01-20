from flask import Flask, render_template, url_for, request, redirect

app = Flask(__name__)


class Usuario():
	def __init__(self, usuario, senha):
		self.usuario = usuario
		self.senha = senha
	
	
@app.route("/", methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		with open("data.txt", 'r') as f:
			for linha in f:
				usuario = ""
				i = 0
				while (linha[i] != " "):
					usuario += linha[i]
					i += 1
				if (usuario == request.form["username"]):
					i += 1
					senha = ""
					for j in range(i, len(linha)):
						senha += linha[j]
					if (senha == request.form["password"]):
						return render_template("planetas.html")
					else:
						print("Senha inválida")
				else:
					print("Usuário inválido")
					 
	return render_template("login.html")

@app.route("/registrar", methods=['GET', 'POST'])
def registro():
	if request.method == 'POST':
		info = [request.form["username"], request.form["password"]]
		with open("data.txt", 'w') as f:
			f.write(" ".join(info))
		return render_template("planetas.html")
	return render_template("registro.html")

@app.route("/planetas")
def planetas():
	return render_template("planetas.html")

if __name__ == "__main__":
	app.run(debug=True)
