from flask import Flask, jsonify, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://qqoqrjyiraaihu:f61c12db707726912880ce22d6e3cccd86c4d7d579db21da79098c3e75a2d486@ec2-18-209-187-54.compute-1.amazonaws.com:5432/d4u87pn01tgc5b'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

n_planetas = 0
n_estrelas = 0
n_satelites = 0
n_sistemas = 0

def get_obj(ls, tipo):
    r = []

    if ls == None:
        return r

    if tipo == "planeta":
        for ele in ls:
            r.append(Planeta.query.get(ele))
    elif tipo == "satelite":
        for ele in ls:
            r.append(Satelite.query.get(ele))
    elif tipo == "galaxia":
        for ele in ls:
            r.append(Galaxia.query.get(ele))
    elif tipo == "sistema":
        for ele in ls:
            r.append(Sistema.query.get(ele))
    else:
        for ele in ls:
            r.append(Estrela.query.get(ele))
            
    return r

def get_id(ls):
    if ls == None:
        return None

    r = []

    for ele in ls:
        r.append(ele.id)
           
    return r

def from_bool(val):
    if val == True:
        return "Sim"
    return "Não"

def to_bool(val):
    if val == "Sim":
        return True
    return False

def to_none(msg):
    if msg == '':
        return None
    return msg

class Dados(db.Model):
    __tablename__ = 'dados'
    id = db.Column('id', db.Integer, primary_key=True)
    n_planetas = db.Column('n_planetas', db.Integer)
    n_satelites = db.Column('n_satelites', db.Integer)
    n_galaxias = db.Column('n_galaxias', db.Integer)
    n_sistemas = db.Column('n_sistemas', db.Integer)
    n_estrelas = db.Column('n_estrelas', db.Integer)

    def __init__(self):
        self.n_planetas = 0
        self.n_satelites = 0
        self.n_galaxias = 0
        self.n_sistemas = 0
        self.n_estrelas = 0

class Usuario(db.Model):
    __tablename__ = 'usuario'
    login = db.Column('klogin', db.Unicode, primary_key=True)
    senha = db.Column('kpassword', db.Unicode)
    
    def __init__(self, login, senha):
        self.login = login
        self.senha = senha


class Galaxia(db.Model):
    __tablename__ = 'galaxia'
    id = db.Column('id_galaxia', db.Integer, primary_key=True)
    nome = db.Column('nome', db.Unicode)
    qt_sistema = db.Column('qt_sistema', db.Integer)
    dist_terra = db.Column('dist_terra', db.Float)

    def __init__(self, nome, qt_sistema=None, dist_terra=None):
        self.nome = nome
        self.qt_sistema = qt_sistema
        self.dist_terra = dist_terra

    def header_infos(self):
        return {"id": self.id, "Nome": self.nome}

    def infos(self):
        return {"Quantidade sistema": self.qt_sistema, "Distância até a terra": self.dist_terra}
        
    def pegar_sistemas(self):
        sistemas = Sistema.query.all()
        ids = list()

        for sistema in sistemas:
            ids.append(sistema.id_sistema)

        return ids

    def infos_tipos(self):
        return {"tam": 3,
                "tipo": "galaxia",
                "type_atribs": ["string", "int", "float"],
                "label_atribs": ["Nome", "Quantidade de sistemas", "Distância até a terra"],
                "atribs": [{"nome": self.nome},
                           {"qt_sistema": self.qt_sistema}, 
                           {"dist_terra": self.dist_terra}]}


sistema_estrela = db.Table('sistema_estrela',
            db.Column('sistema_id', db.Integer, db.ForeignKey('sistema.id_sistema')),
            db.Column('estrela_id', db.Integer, db.ForeignKey('estrela.id_estrela')))
            
sistema_planeta = db.Table('sistema_planeta',
            db.Column('sistema_id', db.Integer, db.ForeignKey('sistema.id_sistema')),
            db.Column('planeta_id', db.Integer, db.ForeignKey('planeta.id_planeta')))


class Sistema(db.Model):
    __tablename__ = 'sistema'
    id = db.Column('id_sistema', db.Integer, primary_key=True)
    nome = db.Column('nome', db.Unicode)
    qt_planetas = db.Column('qt_planetas', db.Integer)
    qt_estrelas = db.Column('qt_estrelas', db.Integer)
    idade = db.Column('idade', db.Integer)
    galaxia_id = db.Column('galaxia', db.Integer, db.ForeignKey('galaxia.id_galaxia'), nullable=False)

    sistema_estrelas = db.relationship('Estrela', secondary=sistema_estrela, backref=db.backref('estrela_sistemas'))
    
    def __init__(self, nome, galaxia_id, qt_planetas, qt_estrelas, idade, sistema_estrelas, sistema_planetas):
        self.nome = nome
        self.qt_planetas = qt_planetas
        self.qt_estrelas = qt_estrelas
        self.idade = idade
        self.galaxia_id = galaxia_id
        self.sistema_estrelas = sistema_estrelas
        self.sistema_planetas = sistema_planetas

    def header_infos(self):
        return {"id": self.id, "Nome": self.nome}

    def infos(self):
        return {"Quantidade de planetas": self.qt_planetas, "Quantidade de estrelas": self.qt_estrelas, "Idade": self.idade, "Pertence à galáxia": self.galaxia_id, "Pertence às estrelas": get_id(self.sistema_estrelas), "Possui os planetas": get_id(self.sistema_planetas)}
        
    def pegar_estrelas(self):
        ests = Estrela.query.all()
        ls = []
        for est in ests:
            ls.append(est.id)
        return ls
    
    def pegar_galaxias(self):
        gals = Galaxia.query.all()
        ls = []

        for gal in gals:
            ls.append(gal.id) 
        return ls

    def pegar_planetas(self):
        planetas = Planeta.query.all()
        ids = list()
        
        for planeta in planetas:
            ids.append(planeta.id) 
        return ids

    def infos_tipos(self):
        return {"tam": 7,
                "tipo": "sistema",
                "arrays": [0, 0, 0, 0, self.pegar_galaxias(), self.pegar_estrelas(), self.pegar_planetas()],
                "type_atribs": ["string", "int", "int", "int", "array", "multi_array", "multi_array"],
                "label_atribs": ["Nome", "Quantidade de planetas", "Quantidade de estrelas", "Idade", "Pertence à galáxia", "Pertence às estrelas", "Possui os planetas"],
                "atribs": [{"nome": self.nome},
                           {"qt_planetas": self.qt_planetas},
                           {"qt_estrelas": self.qt_estrelas},
                           {"idade": self.idade},
                           {"galaxia_id": self.galaxia_id},
                           {"sistema_estrelas": get_id(self.sistema_estrelas)},
                           {"sistema_planetas": get_id(self.sistema_planetas)}]}


orbitar = db.Table('orbitar',
        db.Column('satelite_id', db.Integer, db.ForeignKey('satelite.id_satelite')),
        db.Column('planeta_id', db.Integer, db.ForeignKey('planeta.id_planeta')),
        db.Column('estrela_id', db.Integer, db.ForeignKey('estrela.id_estrela')))


class Estrela(db.Model):
    __tablename__ = 'estrela'
    id = db.Column('id_estrela', db.Integer, primary_key=True)
    nome = db.Column('nome', db.Unicode)
    tamanho = db.Column('tamanho', db.Float)
    idade = db.Column('idade', db.Integer)
    possui_estrela = db.Column('possui_estrela', db.Boolean)
    dist_terra = db.Column('dist_terra', db.Float)
    tipo_estrela = db.Column('tipo', db.Enum('Anã Branca', 'Anã Vermelha', 'Estrela Binária', 'Gigante Azul', 'Gigante Vermelha'), nullable=False)

    estrela_orb_planetas = db.relationship('Planeta', secondary=orbitar, backref=db.backref('planeta_orb_estrelas'))

    # gigante_vermelha = db.relationship('GiganteVermelha', uselist=False)
    
    def __init__(self, nome, tipo, tamanho, idade, possui_estrela, dist_terra, estrela_sistemas):
        self.nome = nome
        self.tipo_estrela = tipo
        self.tamanho = tamanho
        self.idade = idade
        self.possui_estrela = possui_estrela
        self.dist_terra = dist_terra
        self.estrela_sistemas = estrela_sistemas

    def header_infos(self):
        return {"id": self.id, "Nome": self.nome}

    def infos(self):
        return {"Tipo": self.tipo_estrela, "Tamanho": self.tamanho, "Idade": self.idade, "Possui estrela": self.possui_estrela, "Distância até a terra": self.dist_terra, "Possui os sistemas": get_id(self.estrela_sistemas), "É orbitado pelos satélites": get_id(self.estrela_orb_satelites), "É orbitado pelos planetas": get_id(self.estrela_orb_planetas)}

    def pegar_planetas(self):
        planetas = Planeta.query.all()
        ids = list()
        
        for planeta in planetas:
            ids.append(planeta.id) 

        return ids

    def pegar_satelites(self):
        satelites = Satelite.query.all()
        ids = list()

        for satelite in satelites:
            ids.append(satelite.id_satelite)

        return ids

    def pegar_sistemas(self):
        sistemas = Sistema.query.all()
        ids = list()
        for sistema in sistemas:
            ids.append(sistema.id)
        return ids
    
    def infos_tipos(self):
        return {"tam": 8,
                "tipo": "estrela",
                "arrays": [0, 0, 0, ["Sim", "Não"], 0, self.pegar_sistemas(), self.pegar_satelites(), self.pegar_planetas()],
                "type_atribs": ["string", "float", "int", "array", "float", "multi_array", "multi_array", "multi_array"],
                "label_atribs": ["Nome", "Tamanho", "Idade", "Possui estrela", "Distância até a terra", "Possui os sistemas", "É orbitado pelos satélites", "É orbitado pelos planetas"],
                "atribs": [{"nome": self.nome},
                           {"tamanho": self.tamanho},
                           {"idade": self.idade},
                           {"possui_estrela": from_bool(self.possui_estrela)},
                           {"dist_terra": self.dist_terra},
                           {"estrela_sistemas": get_id(self.estrela_sistemas)},
                           {"estrela_orb_satelites": get_id(self.estrela_orb_satelites)},
                           {"estrela_orb_planetas": get_id(self.estrela_orb_planetas)}]}


class Planeta(db.Model):
    __tablename__ = 'planeta'
    id = db.Column('id_planeta', db.Integer, primary_key=True)
    nome = db.Column('nome', db.Unicode)
    tamanho = db.Column('tamanho', db.Float)
    peso = db.Column('peso', db.Float)
    vel_rotacao = db.Column('vel_rotacao', db.Float)
    possui_sn = db.Column('possui_sn', db.Boolean)
    comp_planeta = db.Column('comp_planeta', db.Unicode)
    
    planeta_sistemas = db.relationship('Sistema', secondary=sistema_planeta, backref=db.backref('sistema_planetas'))
    planeta_orb_satelites = db.relationship('Satelite', secondary=orbitar, backref=db.backref('satelite_orb_planetas'))

    def __init__(self, nome, tamanho, peso, comp_planeta, possui_sn, vel_rotacao, planeta_sistemas):
        self.nome = nome
        self.tamanho = tamanho
        self.peso = peso
        self.comp_planeta = comp_planeta
        self.possui_sn = possui_sn
        self.vel_rotacao = vel_rotacao
        self.planeta_sistemas = planeta_sistemas
        
    def header_infos(self):
        return {"id": self.id, "Nome": self.nome}
       
    def pegar_sistemas(self):
        sists = Sistema.query.all()
        ls = []

        for sist in sists:
            ls.append(sist.id)
        return ls

    def pegar_satelites(self):
        satelites = Satelite.query.all()
        ids = list()

        for satelite in satelites:
            ids.append(satelite.id)
        return ids

    def pegar_estrelas(self):
        estrelas = Estrela.query.all()
        ids = list()

        for estrela in estrelas:
            ids.append(estrela.id)
        return ids


    def infos(self):
        print(self.planeta_sistemas)
        return {"Tamanho": self.tamanho, "Peso": self.peso, "Velocidade de rotação": self.vel_rotacao, "Possui satélite natural": self.possui_sn, "Composição do planeta": self.comp_planeta, "Pertence aos sistemas": get_id(self.planeta_sistemas), "É orbitado pelos satélites": get_id(self.planeta_orb_satelites), "Orbita as estrelas": get_id(self.planeta_orb_estrelas)}
        
    def infos_tipos(self):
        return {"tam": 9,
                "tipo": "planeta",
                "arrays": [0, 0, 0, 0, ["Sim", "Não"], 0, self.pegar_sistemas(), self.pegar_satelites(), self.pegar_estrelas()],
                "type_atribs": ["string", "float", "float", "float", "array", "string", "multi_array", "multi_array", "multi_array"],
                "label_atribs": ["Nome", "Tamanho", "Peso", "Velocidade de rotação", "Possui satélite natural", "Composição do planeta", "Pertence aos sistemas", "É orbitado pelos satélites", "Orbita as estrelas"],
                "atribs": [{"nome": self.nome},
                           {"tamanho": self.tamanho},
                           {"peso": self.peso},
                           {"vel_rotacao": self.vel_rotacao},
                           {"possui_sn": from_bool(self.possui_sn)},
                           {"comp_planeta": self.comp_planeta},
                           {"planeta_sistemas": get_id(self.planeta_sistemas)},
                           {"planeta_orb_satelites": get_id(self.planeta_orb_satelites)},
                           {"planeta_orb_estrelas": get_id(self.planeta_orb_estrelas)}]}


class Satelite(db.Model):
    __tablename__ = 'satelite'
    id = db.Column('id_satelite', db.Integer, primary_key=True)
    nome = db.Column('nome', db.Unicode)
    tamanho = db.Column('tamanho', db.Float)
    peso = db.Column('peso', db.Float)
    comp_sn = db.Column('comp_sn', db.Unicode)

    satelite_orb_estrelas = db.relationship('Estrela', secondary=orbitar, backref=db.backref('estrela_orb_satelites'))

    def __init__(self, nome, tamanho, peso, comp_sn):
        self.nome = nome
        self.tamanho = tamanho
        self.peso = peso
        self.comp_sn = comp_sn
        
    def header_infos(self):
        return {"id": self.id, "Nome": self.nome}
        
    def infos(self):
        return {"Tamanho": self.tamanho, "Peso": self.peso, "Composição": self.comp_sn, "Orbita as estrelas": get_id(self.satelite_orb_estrelas), "Orbita os planetas": get_id(self.satelite_orb_planetas)}

    def infos_tipos(self):
        return {"tam": 6,
                "tipo": "satelite",
                "type_atribs": ["string", "flaot", "float", "string", "multi_array", "multi_array"],
                "label_atribs": ["Nome", "Tamanho", "Peso", "Composição", "Orbita as estrelas", "Orbita os planetas"],
                "atribs": [{"nome": self.nome},
                           {"tamanho": self.tamanho},
                           {"peso": self.peso},
                           {"comp_satelite": self.comp_satelite},
                           {"satelite_orb_estrelas": get_id(self.satelite_orb_estrelas)},
                           {"satelite_orb_planetas": get_id(self.satelite_orb_planetas)}]}


class GiganteVermelha(db.Model):
    __tablename__ = 'gigante_vermelha'
    estrela_id = db.Column('estrela', db.Integer, db.ForeignKey('id_estrela'), primary_key=True, nullable=False)
    morte = db.Column('morte', db.Boolean, nullable=False)

    def __init__(self):
        self.morte = False

def pegar_entidade(tipo):
    if tipo == "planeta":
        entidades = Planeta.query.all()
    elif tipo == "estrela":
        entidades = Estrela.query.all()
    elif tipo == "satelite":
        entidades = Satelite.query.all()
    elif tipo == "sistema":
        entidades = Sistema.query.all()
    else:
        entidades = Galaxia.query.all()

    ls = []
    for ent in entidades:
        ls.append(ent.id)
    return ls

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if len(Dados.query.all()) == 0:
            db.session.add(Dados())
            db.session.commit()

        login = request.form["username"]
        senha = request.form["password"]
        
        usuario = Usuario.query.get(login)
        if (usuario == None or usuario.senha != senha):
            return render_template("login.html", tipo="error")
        return redirect("entidades")
    return render_template("login.html", tipo="hidden")

@app.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == "POST":
        if len(Dados.query.all()) == 0:
            db.session.add(Dados())
            db.session.commit()

        login = request.form["username"]
        senha = request.form["password"]
        
        usuario = Usuario.query.get(login)
        if (usuario != None):
            return redirect("registro.html", tipo="error")
        db.session.add(Usuario(login, senha))
        db.session.commit()
        return redirect("entidades")
    return render_template("registro.html", tipo="hidden")

@app.route("/entidades", methods=["GET", "POST"])
def entidades():
    
    if request.method == "POST" and "add" in request.form:
        nome = request.form["nome"]
        tipo = request.form["tipo"]
        
        if tipo == "planeta":
            tamanho = to_none(request.form["tamanho"])
            peso = to_none(request.form["peso"])
            comp_planeta = to_none(request.form["comp_planeta"])
            possui_sn = to_bool(request.form["possui_sn"])
            vel_rotacao = to_none(request.form["vel_rotacao"])

            db.session.add(Planeta(nome, tamanho, peso, comp_planeta, possui_sn, vel_rotacao, []))
            db.session.commit()

            
            Dados.query.get(1).n_planetas = Dados.query.get(1).n_planetas + 1
            db.session.commit()

            tmp = Planeta.query.get("planeta" + str(Dados.query.get(1).n_planetas))
            tmp.planeta_sistemas = get_obj(request.form.getlist("planeta_sistemas"), "sistema")
            tmp.planeta_orb_estrelas = get_obj(request.form.getlist("planeta_orb_estrelas"), "estrela")
            tmp.planeta_orb_satelites = get_obj(request.form.getlist("planeta_orb_satelites"), "satelite")
        elif tipo == "sistema":
            galaxia_id = request.form["galaxia_id"]
            qt_estrelas = to_none(request.form["tamanho"])
            qt_planetas = to_none(request.form["qt_planetas"])
            idade = to_none(request.form["idade"])
            
            db.session.add(Sistema(nome, galaxia_id, qt_planetas, qt_estrelas, idade, [], []))
            db.session.commit()

            Dados.query.get(1).n_sistemas = Dados.query.get(1).n_sistemas + 1
            db.session.commit()

            tmp = Sistema.query.get("sistema" + str(Dados.query.get(1).n_sistemas))
            tmp.sistema_estrelas = get_obj(request.form.getlist("sistema_estrelas"), "estrela")
            tmp.sistema_planetas = get_obj(request.form.getlist("sistema_planetas"), "planeta") 
        elif tipo == "estrela":
            tipo_estrela = request.form["tipo_estrela"]
            tamanho = to_none(request.form["tamanho"])
            idade = to_none(request.form["idade"])
            possui_estrela = to_bool(request.form["possui_estrela"])
            dist_terra = to_none(request.form["dist_terra"])
            
            db.session.add(Estrela(nome, tipo_estrela, tamanho, idade, possui_estrela, dist_terra, []))
            db.session.commit()
            
            Dados.query.get(1).n_estrelas = Dados.query.get(1).n_estrelas + 1
            db.session.commit()

            tmp = Estrela.query.get("estrela" + str(Dados.query.get(1).n_estrelas))
            tmp.estrela_sistemas = get_obj(request.form.getlist("estrela_sistemas"), "sistema")
            tmp.estrela_orb_planetas = get_obj(request.form.getlist("estrela_orb_planetas"), "planeta")
            tmp.estrela_orb_satelites = get_obj(request.form.getlist("estrela_orb_satelites"), "satelite")
        elif tipo == "galaxia":
            qt_sistema = to_none(request.form["qt_sistema"])
            dist_terra = to_none(request.form["dist_terra"])
            
            db.session.add(Galaxia(nome, qt_sistema, dist_terra))
        else:
            tamanho = to_none(request.form["tamanho"])
            peso = to_none(request.form["peso"])
            comp_sn = to_none(request.form["comp_sn"])
            
            db.session.add(Satelite(nome, tamanho, peso, comp_sn))
            db.session.commit()

            Dados.query.get(1).n_satelites = Dados.query.get(1).n_satelites + 1
            db.session.commit()

            tmp = Satelite.query.get("satelite" + str(Dados.query.get(1).n_satelites))
            tmp.satelite_orb_planetas = get_obj(request.form.getlist("satelite_orb_planetas"), "planeta")
            tmp.satelite_orb_estrelas = get_obj(request.form.getlist("satelite_orb_estrelas"), "estrela")
       
        db.session.commit()
    # MODIFICAR !!!
    elif request.method == "POST" and "mod" in request.form:
        iden = request.form["id"]
        tipo = request.form["tipo"]
        
        if tipo == "planeta":
            planeta = Planeta.query.get(iden)
            print(planeta)
            
            planeta.nome = request.form["nome"]
            planeta.tamanho = request.form["tamanho"]
            planeta.peso = request.form["peso"]
            planeta.comp_planeta = request.form["comp_planeta"]
            planeta.possui_sn = to_bool(request.form["possui_sn"])
            planeta.vel_rotacao = request.form["vel_rotacao"]
            planeta.planeta_sistemas = get_obj(request.form.getlist("planeta_sistemas"), "sistema")
            planeta.planeta_orb_estrelas = get_obj(request.form.getlist("planeta_orb_estrelas"), "estrela")
            planeta.planeta_orb_satelites = get_obj(request.form.getlist("planeta_orb_satelites"), "satelite")
        elif tipo == "sistema":
            sistema = Sistema.query.get(iden)
            
            sistema.nome = request.form["nome"]
            sistema.galaxia_id = request.form["galaxia_id"]
            sistema.qt_estrelas = request.form["tamanho"]
            sistema.qt_planetas = request.form["qt_planetas"]
            sistema.idade = request.form["idade"]
            sistema.sistema_planetas = get_obj(request.form.getlist("sistema_planetas"), "planeta")
            sistema.sistema_estrelas = get_obj(request.form.getlist("sistema_estrelas"), "estrela")
        elif tipo == "estrela":
            estrela = Estrela.query.get(iden)
            
            estrela.nome = request.form["nome"]
            estrela.tamanho = request.form["tamanho"]
            estrela.idade = request.form["idade"]
            estrela.possui_estrela = to_bool(request.form["possui_estrela"])
            estrela.dist_terra = request.form["dist_terra"]
            estrela.estrela_sistemas = get_obj(request.form.getlist("estrela_sistemas"), "sistema")
            estrela.estrela_orb_planetas = get_obj(request.form.getlist("estrela_orb_planetas"), "planeta")
            estrela.estrela_orb_satelites = get_obj(request.form.getlist("estrela_orb_satelites"), "satelite")
        elif tipo == "galaxia":
            galaxia = Galaxia.query.get(iden)
            
            galaxia.nome = request.form["nome"]
            galaxia.qt_sistema = request.form["qt_sistema"]
            galaxia.dist_terra = request.form["dist_terra"]
        else:
            satelite = Satelite.query.get(iden)
            
            satelite.nome = request.form["nome"]
            satelite.tamanho = request.form["tamanho"]
            satelite.peso = request.form["peso"]
            satelite.comp_sn = request.form["comp_sn"]
            satelite.satelite_orb_planetas = get_obj(request.form.getlist("satelite_orb_planetas"), "planeta")
            satelite.satelite_orb_estrelas = get_obj(request.form.getlist("satelite_orb_estrelas"), "estrela")
        
        db.session.commit()
    elif request.method == "POST":
        print("aqui")
        return '', 204
    return render_template("entidades.html", nome='', filtros=[])

@app.route("/entidades/get_entidades", methods=["POST"])
def get_entidades():
    if request.method == "POST":
        data = request.get_json()
        print(data)
        nome = data["nome"]
        filtros = data["filtros"]
        
        planetas = []
        galaxias = []
        sistemas = []
        satelites = []
        estrelas = []
        
        if filtros["planeta"]:
            planetas = Planeta.query.filter(Planeta.nome.like('%' + nome + '%')).all()
        if filtros["galaxia"]:
            galaxias = Galaxia.query.filter(Galaxia.nome.like('%' + nome + '%')).all()
        if filtros["sistema"]:
            sistemas = Sistema.query.filter(Sistema.nome.like('%' + nome + '%')).all()
        if filtros["satelite"]:
            satelites = Satelite.query.filter(Satelite.nome.like('%' + nome + '%')).all()
        if filtros["estrela"]:
            estrelas = Estrela.query.filter(Estrela.nome.like('%' + nome + '%')).all()
            
        ls = []
            
        for pla in planetas:
            ls.append(pla.header_infos())
        for gal in galaxias:
            ls.append(gal.header_infos())
        for sis in sistemas:
            ls.append(sis.header_infos())
        for sat in satelites:
            ls.append(sat.header_infos())
        for est in estrelas:
            ls.append(est.header_infos())

        return jsonify(ls)

@app.route("/entidades/get_infos", methods=["POST"])
def get_infos():
    if request.method == "POST":
        req_id = request.get_json()
        i = 0
        while (not req_id[i].isdigit()):
            i += 1
        tipo = req_id[0: i]

        if tipo == "planeta":
            infos = Planeta.query.get(req_id).infos()
        elif tipo == "estrela":
            infos = Estrela.query.get(req_id).infos()
        elif tipo == "satelite":
            infos = Satelite.query.get(req_id).infos()
        elif tipo == "galaxia":
            infos = Galaxia.query.get(req_id).infos()
        else:
            infos = Sistema.query.get(req_id).infos()

        print(infos)
        return jsonify(infos)
        
@app.route("/entidades/all_types", methods=["GET"])
def all_types():
    if request.method == "GET":
        return jsonify(
            {"tam_tipos": 5,
             "tipos": [{"Planeta": "planeta"}, {"Satélite natural": "satelite"}, {"Estrela": "estrela"}, {"Galáxia": "galaxia"}, {"Sistema planetário": "sistema"}],
             "tam_atribs": 25,
             "atribs": [{"info": "Nome", "tipo": "string", "valor": "nome", "null": False},
                        {"info": "Tamanho", "tipo": "float", "valor": "tamanho", "null": True}, 
                        {"info": "Peso", "tipo": "float", "valor": "peso", "null": True},
                        {"info": "Velocidade de rotação", "tipo": "float", "valor": "vel_rotacao", "null": True},
                        {"info": "Possui satélite natural", "tipo": "bool", "valor": "possui_sn", "null": True},
                        {"info": "Composição do planeta", "tipo": "string", "valor": "comp_planeta", "null": True},
                        {"info": "Composição do satélite natural", "tipo": "string", "valor": "comp_sn", "null": True},
                        {"info": "Idade", "tipo": "int", "valor": "idade", "null": True},
                        {"info": "Possui estrela", "tipo": "array", "valor": "possui_estrela", "array": ["Sim", "Não"], "null": True},
                        {"info": "Quantidade sistemas", "tipo": "int", "valor": "qt_sistema", "null": True}, 
                        {"info": "Quantidade de planetas", "tipo": "int", "valor": "qt_planetas", "null": True},
                        {"info": "Quantidade de estrelas", "tipo": "int", "valor": "qt_estrelas", "null": True},
                        {"info": "Distância até a terra", "tipo": "float", "valor": "dist_terra", "null": True},
                        {"info": "Pertence à galáxia", "tipo": "array", "valor": "galaxia_id", "array": pegar_entidade("galaxia"), "null": True},
                        {"info": "Possui os planetas", "tipo": "multi_array", "valor": "sistema_planetas", "array": pegar_entidade("planeta"), "null": True},
                        {"info": "Pertence aos sistemas", "tipo": "multi_array", "valor": "planeta_sistemas", "array": pegar_entidade("sistema"), "null": True},
                        {"info": "Possui os sistemas", "tipo": "multi_array", "valor": "estrela_sistemas", "array": pegar_entidade("sistema"), "null": True},
                        {"info": "Pertence às estrelas", "tipo": "multi_array", "valor": "sistema_estrelas", "array": pegar_entidade("estrela"), "null": True},
                        {"info": "É orbitado pelos satélites", "tipo": "multi_array", "valor": "planeta_orb_satelites", "array": pegar_entidade("satelite"), "null": True},
                        {"info": "Orbita as estrelas", "tipo": "multi_array", "valor": "planeta_orb_estrelas", "array": pegar_entidade("estrela"), "null": True},
                        {"info": "Orbita os planetas", "tipo": "multi_array", "valor": "satelite_orb_planetas", "array": pegar_entidade("planeta"), "null": True},
                        {"info": "Orbita as estrelas", "tipo": "multi_array", "valor": "satelite_orb_estrelas", "array": pegar_entidade("estrela"), "null": True},
                        {"info": "É orbitado pelos planetas", "tipo": "multi_array", "valor": "estrela_orb_planetas", "array": pegar_entidade("planeta"), "null": True},
                        {"info": "É orbitado pelos satélites", "tipo": "multi_array", "valor": "estrela_orb_satelites", "array": pegar_entidade("satelite"), "null": True}, 
                        {"info": "Tipo", "tipo": "string", "valor": "tipo_estrela", "null": True}],
             "vis_atribs": [True, True, True, True, True, True, False, False, False, False, False, False, False, False, False, True, False, False, True, True, False, False, False, False, False]}
        )

@app.route("/entidades/get_infos_tipos", methods=["POST"])
def get_infos_tipos():
    if request.method == "POST":
        req_id = request.get_json()
        i = 0
        while (not req_id[i].isdigit()):
            i += 1
        tipo = req_id[0: i]

        print(req_id)

        infos = {}
        if tipo == "planeta":
            infos = Planeta.query.get(req_id).infos_tipos()
        elif tipo == "galaxia":
            infos = Galaxia.query.get(req_id).infos_tipos()
        elif tipo == "satelite":
            infos = Satelite.query.get(req_id).infos_tipos()
        elif tipo == "sistema":
            infos = Sistema.query.get(req_id).infos_tipos()
        elif tipo == "estrela":
            infos = Estrela.query.get(req_id).infos_tipos()
        
        return jsonify(infos)


@app.route("/entidade/remove_entidade", methods=["POST"])
def remover_entidade():
    print("aqui")
    if request.method == "POST":
        req_id = request.get_json()
        i = 0
        while (not req_id[i].isdigit()):
            i += 1
        tipo = req_id[0: i]
        
        print(type(req_id))
        
        if tipo == "planeta":
            Planeta.query.filter_by(id = req_id).delete()
        elif tipo == "galaxia":
            Galaxia.query.filter_by(id = req_id).delete()
        elif tipo == "sistema":
            Sistema.query.filter_by(id = req_id).delete()
        elif tipo == "satelite":
            Satelite.query.filter_by(id = req_id).delete()
        elif tipo == "estrela":
            Estrela.query.filter_by(id = req_id).delete()
        db.session.commit()
        
        return '', 204


@app.route("/entidade/busca_entidade", methods=["POST"])
def busca():
    if request.method == "POST":
        entidade = request.form["busca"]
        planeta = Planeta.query.get(entidade)
        atributos = dict()

        if planeta:
            atributos["nome"] = planeta.nome
            atributos["tamanho"] = planeta.tamanho
            atributos["peso"] = planeta.peso
            atributos["comp_planeta"] = planeta.comp_planeta
            atributos["possui_sn"] = planeta.possui_sn
            atributos["vel_rotacao"] = planeta.vel_rotacao
        else:
            atributos["nome"] = "Planeta inexistente ou não cadastrado!"

        return jsonify(atributos)


if __name__ == "__main__":
    app.run(threaded=True, debug=True, port=5000)
