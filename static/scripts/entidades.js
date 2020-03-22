async function print_infos(id) {
    let mini_header = document.getElementById(id);
    mini_header.onclick = null;
    
    let data = id;
    console.log(data)
    var options = {
        method: "POST",
        headers: {
            "Content-type": "application/json"
        },
        body: JSON.stringify(data)
    };
    let response = await fetch("/entidades/get_infos", options);
    
    if (response.ok) {
        let infos = await response.json();
        
        console.log(infos)
        
        let div = document.createElement("div");
        div.id = "infos-" + id;
        
        for (const [key, value] of Object.entries(infos)) {
            let p = document.createElement("p");
            p.innerHTML = key.concat(": ".concat(value));
            
            div.appendChild(p);
        }
        
        mini_header.appendChild(div);
        mini_header.onclick = function() {hide_infos(this.id);};
    }
}

function hide_infos(id) {
    let mini_header = document.getElementById(id);
    let infos = document.getElementById("infos-" + id);
    mini_header.removeChild(infos);
    mini_header.onclick = function() {print_infos(this.id);};
}

async function remover_entidade(id) {
    console.log("aqui");
    
    let div = document.getElementById(id);
    div.parentNode.removeChild(div);
    
    console.log(id);
    
    let data = id;
    let options = {
        method: "POST",
        headers: {
            "Content-type": "application/json"
        },
        body: JSON.stringify(data)
    };
    
    let response = await fetch("/entidade/remove_entidade", options);
}

async function get_entidades() {
    let response = await fetch("/entidades/get_entidades");
    
    if (response.ok) {
        let entidades = await response.json();
        let len = entidades.length;
        let parentDiv = document.createElement("div");
        
        for (let i = 0; i < len; i++) {
            let obj = entidades[i];
            console.log(obj);
            
            let div = document.createElement("div");
            div.className = "mini-cabecalho";
            div.style.cursor = "pointer";
            div.id = obj["id"];
            div.onclick = function() {print_infos(this.id);};
        
            let div_esq = document.createElement("div");
            div_esq.className = "canto-esq";
            let div_dir = document.createElement("div");
            div_dir.className = "canto-dir";
            
            let nome = document.createElement("span"); 
            nome.innerHTML = "Nome: ".concat(obj["Nome"]);
            div_esq.appendChild(nome);
            
            div_esq.appendChild(document.createElement("br"));
            
            let id = document.createElement("span");
            id.innerHTML = "#".concat(obj["id"]);
            div_esq.appendChild(id);
    
            let remover = document.createElement("span");
            remover.className = "close canto-dir";
            remover.innerHTML = "&times";
            remover.onclick = function() {remover_entidade(obj["id"])};
            div_dir.appendChild(remover);
    
            div.appendChild(div_esq);
            div.appendChild(div_dir);
    
            parentDiv.appendChild(div);
        }
        
        document.body.appendChild(parentDiv);
    }
}

function atualizar_campos() {
    let tipo = document.getElementById("tipo").value;
    
    let nome = document.getElementById("nome");
    let qt_estrelas = document.getElementById("qt_estrelas");
    let qt_planetas = document.getElementById("qt_planetas");
    let qt_sistema = document.getElementById("qt_sistema");
    let dist_terra = document.getElementById("dist_terra");
    let idade = document.getElementById("idade");
    let tamanho = document.getElementById("tamanho");
    let peso = document.getElementById("peso");
    let comp_planeta = document.getElementById("comp_planeta");
    let comp_sn = document.getElementById("comp_sn");
    let possui_sn = document.getElementById("possui_sn");
    let vel_rotacao = document.getElementById("vel_rotacao");
    let possui_estrela = document.getElementById("possui_estrela");
    
    switch (tipo) {
        case "galaxia":
            nome.style.display = "block";
            qt_estrelas.style.display = "none";
            qt_planetas.style.display = "none";
            qt_sistema.style.display = "block";
            dist_terra.style.display = "block";
            idade.style.display = "none";
            tamanho.style.display = "none";
            peso.style.display = "none";
            comp_planeta.style.display = "none";
            comp_sn.style.display = "none";
            possui_sn.style.display = "none";
            vel_rotacao.style.display = "none";
            possui_estrela.style.display = "none";
            break;
        case "estrela":
            nome.style.display = "block";
            qt_estrelas.style.display = "none";
            qt_planetas.style.display = "none";
            qt_sistema.style.display = "none";
            dist_terra.style.display = "block";
            idade.style.display = "block";
            tamanho.style.display = "block";
            peso.style.display = "none";
            comp_planeta.style.display = "none";
            comp_sn.style.display = "none";
            possui_sn.style.display = "none";
            vel_rotacao.style.display = "none";
            possui_estrela.style.display = "block";
            break;
        case "sistema":
            nome.style.display = "block";
            qt_estrelas.style.display = "block";
            qt_planetas.style.display = "block";
            qt_sistema.style.display = "none";
            dist_terra.style.display = "none";
            idade.style.display = "block";
            tamanho.style.display = "none";
            peso.style.display = "none";
            comp_planeta.style.display = "none";
            comp_sn.style.display = "none";
            possui_sn.style.display = "none";
            vel_rotacao.style.display = "none";
            possui_estrela.style.display = "none";
            break;
        case "planeta":
            nome.style.display = "block";
            qt_estrelas.style.display = "none";
            qt_planetas.style.display = "none";
            qt_sistema.style.display = "none";
            dist_terra.style.display = "none";
            idade.style.display = "none";
            tamanho.style.display = "block";
            peso.style.display = "block";
            comp_planeta.style.display = "block";
            comp_sn.style.display = "none";
            possui_sn.style.display = "block";
            vel_rotacao.style.display = "block";
            possui_estrela.style.display = "none";
            break;
        case "satelite":
            nome.style.display = "block";
            qt_estrelas.style.display = "none";
            qt_planetas.style.display = "none";
            qt_sistema.style.display = "none";
            dist_terra.style.display = "none";
            idade.style.display = "none";
            tamanho.style.display = "block";
            peso.style.display = "block";
            comp_planeta.style.display = "none";
            comp_sn.style.display = "block";
            possui_sn.style.display = "none";
            vel_rotacao.style.display = "none";
            possui_estrela.style.display = "none";
            break;
        default:
            break;
    }
}

function action_adicionar() {
    document.getElementById("add-popup").style.display = "block";
}

function hide_adicionar() {
    document.getElementById("add-popup").style.display = "none";
}

window.onload = function() {
    atualizar_campos();
}

get_entidades();
