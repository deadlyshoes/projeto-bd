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

    sistemas = db.relationship('Sistema', backref='galaxia')

    def __init__(self, nome, qt_sistema, dist_terra):
        self.nome = nome

    def header_infos(self):
        return {"id": self.id, "Nome": self.nome}

    def infos(self):
        return {"Quantidade sistema": self.qt_sistema, "Distância até a terra": self.dist_terra}


sistema_estrela = db.Table('sistema_estrela',
            db.Column('sistema_id', db.Integer, db.ForeignKey('sistema.id_sistema'), primary_key=True)
            db.Column('estrela_id', db.Integer, db.ForeignKey('estrela.id_estrela'), primary_key=True))
sistema_planeta = db.Table('sistema_planeta',
            db.Column('sistema_id', db.Integer, db.ForeignKey('sistema.id_sistema'), primary_key=True)
            db.Column('planeta_id', db.Integer, db.ForeignKey('planeta.id_planeta'), primary_key=True))


class Sistema(db.Model):
    __tablename__ = 'sistema'
    id = db.Column('id_sistema', db.Integer, primary_key=True)
    nome = db.Column('nome', db.Unicode)
    qt_planetas = db.Column('qt_planetas', db.Integer)
    qt_estrelas = db.Column('qt_estrelas', db.Integer)
    idade = db.Column('idade', db.Integer)
    galaxia_id = db.Column('galaxia', db.Integer, db.ForeignKey('galaxia.id_galaxia'), nullable=False)

    estrelas = db.relationship('Estrela', secondary=sistema_estrela)
    planetas = db.relationship('Planeta', secondary=sistema_planeta)
    
    def __init__(self, nome):
        self.nome = nome

    def header_infos(self):
        return {"id": self.id, "Nome": self.nome}

    def infos(self):
        return {"Quantidade de planetas": self.qt_planetas, "Quantidade de estrelas": self.qt_estrelas, "Idade": self.idade}


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

    def header_infos(self):
        return {"id": self.id, "Nome": self.nome}

    def infos(self):
        return {"Tamanho": self.tamanho, "Idade": self.idade, "Possui estrela": self.possui_estrela, "Distância até a terra": self.dist_terra}


class Planeta(db.Model):
    __tablename__ = 'planeta'
    id = db.Column('id_planeta', db.Integer, primary_key=True)
    nome = db.Column('nome', db.Unicode)
    tamanho = db.Column('tamanho', db.Float)
    peso = db.Column('peso', db.Float)
    vel_rotacao = db.Column('vel_rotacao', db.Float)
    possui_sn = db.Column('possui_sn', db.Boolean)
    comp_planeta = db.Column('comp_planeta', db.Unicode)
    
    def __init__(self, nome, tamanho, peso, comp_planeta, possui_sn, vel_rotacao):
        self.nome = nome
        self.tamanho = tamanho
        self.peso = peso
        self.comp_planeta = comp_planeta
        self.possui_sn = True
        self.vel_rotacao = vel_rotacao
        
    def header_infos(self):
        return {"id": self.id, "Nome": self.nome}
        
    def infos(self):
        return {"Tamanho": self.tamanho, "Peso": self.peso, "Velocidade de rotação": self.vel_rotacao, "Possui satélite natural": self.possui_sn, "Composição do planeta": self.comp_planeta}


class Satelite(db.Model):
    __tablename__ = 'satelite'
    id = db.Column('id_satelite', db.Integer, primary_key=True)
    nome = db.Column('nome', db.Unicode)
    tamanho = db.Column('tamanho', db.Float)
    peso = db.Column('peso', db.Float)
    comp_sn = db.Column('comp_sn', db.Unicode)

    def __init__(self, nome):
        self.nome = nome
        
    def header_infos(self):
        return {"id": self.id, "Nome": self.nome}
        
    def infos(self):
        return {"Tamanho": self.tamanho, "Peso": self.peso, "Composição": self.comp_sn}


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
        nome = request.form["nome"]
        tipo = request.form["tipo"]
        
        if tipo == "planeta":
            tamanho = request.form["tamanho"]
            peso = request.form["peso"]
            comp_planeta = request.form["comp_planeta"]
            possui_sn = request.form["possui_sn"]
            vel_rotacao = request.form["vel_rotacao"]
            
            db.session.add(Planeta(nome, tamanho, peso, comp_planeta, possui_sn, vel_rotacao))
        elif tipo == "sistema":
            qt_estrelas = request.form["tamanho"]
            qt_planetas = request.form["qt_planeatas"]
            idade = request.form["idade"]
            
            db.session.add(Sistema(nome))
        elif tipo == "estrela":
            tamanho = request.form["tamanho"]
            idade = request.form["idade"]
            possui_estrela = request.form["possui_estrela"]
            dist_terra = request.form["dist_terra"]
            
            db.session.add(Estrela(nome))
        elif tipo == "galaxia":
            qt_sistema = request.form["qt_sistema"]
            dist_terra = request.form["dist_terra"]
            
            db.session.add(Galaxia(nome))
        else:
            tamanho = request.form["tamanho"]
            peso = request.form["peso"]
            comp_sn = request.form["comp_sn"]
            
            db.session.add(Satelite(nome))
        
        db.session.commit()
        return "done"
    return render_template("entidades.html")

@app.route("/entidades/get_entidades", methods=["GET"])
def get_entidades():
    if request.method == "GET":
        lista = []
        planetas = Planeta.query.all()
        for planeta in planetas:
            lista.append(planeta.header_infos())
        return jsonify(lista)

@app.route("/entidades/get_infos", methods=["POST"])
def get_infos():
    if request.method == "POST":
        req_id = request.get_json()
        i = 0
        while (not req_id[i].isdigit()):
            i += 1
        tipo = req_id[0: i]
        
        infos = {}
        if tipo == "planeta":
            infos = Planeta.query.get(req_id).infos()
        return jsonify(infos)
    
@app.route("/modificar", methods=["GET", "POST"])
def modificar():
    if request.method == "POST":
        nome = request.form["nome"]
        #tipo = request.form["tipo"]
        return redirect("entidades")
    return render_template("modificar.html")

if __name__ == "__main__":
    app.run(threaded=True, debug=True, port=5000)
