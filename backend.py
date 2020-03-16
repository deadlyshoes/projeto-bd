from flask import Flask, jsonify, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://ilmar:@localhost/projeto-bd'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Galaxia(db.Model):
	__tablename__ = 'galaxia'
	id = db.Column('id_galaxia', db.Integer, primary_key=True)
	nome = db.Column('nome', db.Unicode)
	qt_sistema = db.Column('qt_sistema', db.Integer)
	dist_terra = db.Column('dist_terra', db.Float)

	def __init__(self, nome, qt_sistema, dist_terra):
		self.nome = nome

	def infos(self):
		return {"id": self.id, "Nome": self.nome, "Quantidade sistema": self.qt_sistema, "Distância até a terra": self.dist_terra}

class Sistema(db.Model):
	__tablename__ = 'sistema'
	id = db.Column('id_sistema', db.Integer, primary_key=True)
	nome = db.Column('nome', db.Unicode)
	qt_planetas = db.Column('qt_planetas', db.Integer)
	qt_estrelas = db.Column('qt_estrelas', db.Integer)
	idade = db.Column('idade', db.Integer)

	def __init__(self, nome):
		self.nome = nome

	def infos(self):
		return {"id": self.id, "Nome": self.nome, "Quantidade de planetas": self.qt_planetas, "Quantidade de estrelas": self.qt_estrelas, "Idade": self.idade}

class Estrela(db.Model):
	__tablename__ = 'estrela'
	id = db.Column('id_estrela', db.Integer, primary_key=True)
	nome = db.Column('nome', db.Unicode)
	tamanho = db.Column('tamanho', db.Float)
	idade = db.Column('idade', db.Integer)
	possui_estrela = db.Column('possui_estrela', db.Boolean)
	dist_terra = db.Column('dist_terra', db.Float)

	def __init__(self, nome):
		self.nome = nome

	def infos(self):
		return {"id": self.id, "Nome": self.nome, "Tamanho": self.tamanho, "Idade": self.idade, "Possui estrela", self.possui_estrela, "Distância até a terra": self.dist_terra}

class Planeta(db.Model):
	__tablename__ = 'planeta'
	id = db.Column('id_planeta', db.Integer, primary_key=True)
	nome = db.Column('nome', db.Unicode)
	tamanho = db.Column('tamanho', db.Float)
	peso = db.Column('peso', db.Float)
	vel_rotacao = db.Column('vel_rotacao', db.Float)
	possui_sn = db.Column('possui_sn', db.Boolean)
	comp_planeta = db.Column('comp_planeta', db.Unicode)
	
	def __init__(self, nome):
		self.nome = nome
		
	def infos(self):
		return {"id": self.id, "Nome": self.nome, "Tamanho": self.tamanho, "Peso": self.peso, "Velocidade de rotação": self.vel_rotacao, "Possui satélite natural": self.possui_sn, "Composição do planeta": self.comp_planeta}

class Satelite(db.Model):
	__tablename__ = 'satelite'
	id = db.Column('id_satelite', db.Integer, primary_key=True)
	nome = db.Column('nome', db.Unicode)
	tamanho = db.Column('tamanho', db.Float)
	peso = db.Column('peso', db.Float)
	comp_sn = db.Column('comp_sn', db.Unicode)
	
	def __init__(self, nome):
		self.nome = nome
		
	def infos(self):
		return {"id": self.id, "Nome": self.nome, "Tamanho": self.tamanho, "Peso": self.peso, "Composição": self.comp_sn}

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
	planetas = Planeta.query.all()
	return render_template("entidades.html", lista=planetas)

@app.route("/entidades/infos/<tipo>_<i>", methods=["GET", "POST"])
def infos(tipo, i):
	infos = {}
	if tipo == "planeta":
		infos = Planeta.query.get(i).infos()
	return render_template("infos.html", d=infos)

@app.route("/adicionar", methods=["GET", "POST"])
def adicionar():
	if request.method == "POST":
		nome = request.form["nome"]
		tipo = request.form["tipo"]
		
		if tipo == "galaxia":
			db.session.add(Galaxia(nome))
		else if tipo == "sistema":
			db.session.add(Sistema(nome))
		else if tipo == "estrela":
			db.session.add(Estrela(nome))
		else if tipo == "planeta":
			db.session.add(Planeta(nome))
		else:
			db.session.add(Satelite(nome))
		
		db.session.commit()
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
