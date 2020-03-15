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
    dist_terra = db.Column('dist_terra', db.Integer)

    def __init__(self, nome, qt_sistema, dist_terra):
        self.nome = nome
        self.qt_sistema = qt_sistema
        self.dist_terra = dist_terra

    def infos(self):
        return {"id": self.id, "Nome": self.nome, "Quantidade sistema": self.qt_sistema, "Distância até a terra": self.dist_terra}

class Planeta(db.Model):
	__tablename__ = 'planeta'
	id = db.Column('id_planeta', db.Integer, primary_key=True)
	nome = db.Column('nome', db.Unicode)
    tamanho = db.Column('tamanho', db.Integer)
    peso = db.Column('peso', db.Integer)
    vel_rotacao = db.Column('vel_rotacao', db.Integer)
    possui_sn = db.Column('possui_sn', db.Bool)
    comp_planeta = db.Column('comp_planeta', db.Unicode)
	
	def __init__(self, nome):
		self.nome = nome
		
	def infos(self):
        return {"id": self.id, "Nome": self.nome, "Tamanho": self.tamanho, "Peso": self.peso, "Velocidade de rotação": self.vel_rotacao, "Possui satélite natural": self.possui_sn, "Composição do planeta": self.comp_planeta}

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
		if tipo == "planeta":
			db.session.add(Planeta(nome))
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
