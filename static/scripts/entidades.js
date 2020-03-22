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
        div.style.clear = "left";
        
        for (const [key, value] of Object.entries(infos)) {
            let p = document.createElement("p");
            p.innerHTML = key.concat(": ".concat(value));
            
            div.appendChild(p);
        }
        
        mini_header.style.minHeight = "100px";
        mini_header.appendChild(div);
        mini_header.onclick = function() {hide_infos(this.id);};
    }
}

function hide_infos(id) {
    let mini_header = document.getElementById(id);
    let infos = document.getElementById("infos-" + id);
    mini_header.style.minHeight = "20px";
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
            remover.innerHTML = "&#10005";
            remover.onclick = function() {remover_entidade(obj["id"])};
            div_dir.appendChild(remover);
    
            let modificar = document.createElement("span");
            modificar.className = "close canto-dir";
            modificar.innerHTML = "&#9998";
            modificar.onclick = function() {action_modificar(obj["id"])};
            div_dir.appendChild(modificar);
    
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

async function criar_form() {
    console.log("criando formulário...");
    
    let div = document.createElement("div");
    div.className = "add-popup";
    
    let div_content = document.createElement("div");
    div_content.className = "add-popup-content";

    let response = await fetch("/entidades/all_types");
    if (response.ok) {
        let data = await response.json();
        
        console.log(data);
        
        let form = document.createElement("form");
        form.setAttribute("method", "POST");
        
        let len_tipos = data["tam_tipos"];
        let tipos = data["tipos"];
        
        let sel = document.createElement("select");
        sel.setAttribute("name", "tipo");
        sel.setAttribute("onchange", "atualizar_campos()");
        sel.setAttribute("id", "tipo");
        
        for (let i = 0; i < len_tipos; i++) {
            for (const [key, value] of Object.entries(tipos[i])) {
                let opt = document.createElement('option');
                opt.setAttribute("value", value);
                opt.innerHTML = key;
                
                sel.appendChild(opt);
            }
        }
        
        form.appendChild(sel);
        
        let len_atribs = data["tam_atribs"];
        let atribs = data["atribs"];
        let vis_atribs = data["vis_atribs"];
        
        for (let i = 0; i < len_atribs; i++) {
            let atrib = atribs[i];
            
            let field_div = document.createElement("div");
            field_div.id = atrib["valor"];
            
            if (!vis_atribs[i]) {
                field_div.style.display = "none";
            }
            
            let label = document.createElement("div");
            label.setAttribute("for", atrib["valor"]);
            label.innerHTML = atrib["info"];
            
            field_div.appendChild(document.createElement("br"));
            
            let input = document.createElement("input");
            
            switch (atrib["tipo"]) {
                case "int":
                    input.setAttribute("type", "number");
                    break;
                case "float":
                    input.setAttribute("type", "number");
                    break;
                case "string":
                    input.setAttribute("type", "text");
                    break;
                default:
                    break;
            }
            
            input.setAttribute("name", atrib["valor"]);
            
            field_div.appendChild(label);
            field_div.appendChild(input);
            
            form.appendChild(field_div);
        }
        
        let btn = document.createElement("input");
        btn.setAttribute("type", "submit");
        btn.setAttribute("value", "Adicionar");
        form.appendChild(btn);
        
        div_content.appendChild(form);
        
        div.appendChild(div_content);
        
        document.body.appendChild(div);
    }
}

async function action_modificar(id) {
    console.log("aqui");
    
    let div_modal = document.createElement("div");
    div_modal.className = "add-popup";
    
    let div = document.createElement("div");
    div.className = "add-popup-content";
    
    let data = id;
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
        
        console.log(infos);
        
        for (const [key, value] of Object.entries(infos)) {
            let atrib = document.createElement("p");
            atrib.innerHTML = key;
            
            let val_atrib = document.createElement("input");
            val_atrib.setAttribute("type", "text");
            val_atrib.setAttribute("value", value);
            
            div.appendChild(atrib);
            div.appendChild(val_atrib);
        }
    }
    
    let btn_modificar = document.createElement("button");
    div.appendChild(btn_modificar);
    
    div_modal.appendChild(div);
    div_modal.style.display = "block";
    
    document.body.appendChild(div_modal);
}

get_entidades();
