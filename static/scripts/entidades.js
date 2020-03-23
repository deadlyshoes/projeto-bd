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

async function get_entidades(nome, filtros) {
    console.log("aqui");

    let params = {
        "nome": nome,
        "filtros": filtros 
    };
    var options = {
        method: "POST",
        headers: {
            "Content-type": "application/json"
        },
        body: JSON.stringify(params)
    };
    let response = await fetch("/entidades/get_entidades", options);
    
    if (response.ok) {
        let entidades = await response.json();
        let len = entidades.length;
        let parentDiv = document.createElement("div");
        parentDiv.id = "lista-entidades";
        
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
    let sistema_estrelas = document.getElementById("sistema_estrelas");
    let galaxia_id = document.getElementById("galaxia_id");
    let sistema_planetas = document.getElementById("sistema_planetas");
    let estrela_sistemas = document.getElementById("estrela_sistemas");
    let planeta_sistemas = document.getElementById("planeta_sistemas");
    
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
            sistema_estrelas.style.display = "none";
            sistema_planetas.style.display = "none";
            galaxia_id.style.display = "none";
            estrela_sistemas.style.display = "none";
            planeta_sistemas.style.display = "none";
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
            sistema_estrelas.style.display = "none";
            sistema_planetas.style.display = "none";
            galaxia_id.style.display = "none";
            estrela_sistemas.style.display = "block";
            planeta_sistemas.style.display = "none";
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
            sistema_estrelas.style.display = "block";
            sistema_planetas.style.display = "block";
            galaxia_id.style.display = "block";
            estrela_sistemas.style.display = "none";
            planeta_sistemas.style.display = "none";
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
            sistema_estrelas.style.display = "none";
            sistema_estrelas.style.display = "none";
            sistema_planetas.style.display = "none";
            galaxia_id.style.display = "none";
            estrela_sistemas.style.display = "none";
            planeta_sistemas.style.display = "block";
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
            sistema_estrelas.style.display = "none";
            sistema_estrelas.style.display = "none";
            sistema_planetas.style.display = "none";
            galaxia_id.style.display = "none";
            estrela_sistemas.style.display = "none";
            planeta_sistemas.style.display = "none";
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
        form.className = "custom-form";
        
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
            
            let label = document.createElement("label");
            label.setAttribute("for", atrib["valor"]);
            label.innerHTML = atrib["info"];
            
            let input = document.createElement("input");
            switch (atrib["tipo"]) {
                case "int":
                    input.setAttribute("type", "number");
                    break;
                case "float":
                    input.setAttribute("type", "number");
                    input.setAttribute("step", "0.000000000001");
                    break;
                case "string":
                    input.setAttribute("type", "text");
                    break;
                case "array":
                    input = document.createElement("select");
                    let lista = atrib["array"];
                    for (let i = 0; i < lista.length; i++) {
                        let opt = document.createElement('option');
                        opt.setAttribute("value", lista[i]);
                        opt.innerHTML = lista[i];
                        input.appendChild(opt);
                    }
                    break;
                case "multi_array":
                    input = document.createElement("select");
                    input.setAttribute("multiple", "");
                    let ls = atrib["array"];
                    for (let i = 0; i < ls.length; i++) {
                        let opt = document.createElement("option");
                        opt.setAttribute("value", ls[i]);
                        opt.innerHTML = ls[i];
                        input.appendChild(opt);
                    }
                default:
                    break;
            }

            input.setAttribute("name", atrib["valor"]);
            if (!atrib["null"]) {
                input.setAttribute("required", "");
            }
            
            field_div.appendChild(label);
            field_div.appendChild(document.createElement("br"));
            field_div.appendChild(input);
            
            form.appendChild(field_div);
        }
        
        let btn = document.createElement("input");
        btn.setAttribute("type", "submit");
        btn.setAttribute("value", "Adicionar");
        form.appendChild(btn);
        
        let indicator = document.createElement("input");
        indicator.style.display= "none";
        indicator.setAttribute("name", "add");
        form.appendChild(indicator);
        
        div_content.appendChild(form);
        
        div.appendChild(div_content);
        
        document.body.appendChild(div);
    }
}

async function action_modificar(id) {
    console.log("aqui");
    
    let data = id;
    var options = {
        method: "POST",
        headers: {
            "Content-type": "application/json"
        },
        body: JSON.stringify(data)
    };
    let response = await fetch("/entidades/get_infos_tipos", options);
    
    if (response.ok) {
        let infos = await response.json();
        
        console.log(infos);
    
        let div = document.createElement("div");
        div.className = "add-popup";
    
        let div_cont = document.createElement("div");
        div_cont.className = "add-popup-content";
    
        let form = document.createElement("form");
        form.setAttribute("method", "POST");
        form.setAttribute("name", "mod");
        form.className = "custom-form";
        
        let len = infos["tam"];
        let label_atribs = infos["label_atribs"];
        let type_atribs = infos["type_atribs"];
        let atribs = infos["atribs"];
        
        for (let i = 0; i < len; i++) {
            for (const [key, value] of Object.entries(atribs[i])) {
                let label = document.createElement("label");
                label.setAttribute("for", key);
                label.innerHTML = label_atribs[i];
                
                let input = document.createElement("input");
                
                switch (type_atribs[i]) {
                    case "int":
                        input.setAttribute("type", "number");
                        input.setAttribute("value", value);
                        break;
                    case "float":
                        input.setAttribute("type", "number");
                        input.setAttribute("step", "0.000000000001");
                        input.setAttribute("value", value);
                        break;
                    case "string":
                        input.setAttribute("type", "text");
                        input.setAttribute("value", value);
                        break;
                    case "array":
                        input = document.createElement("select");
                        let lista = infos["arrays"][i];
                        console.log(lista);
                        for (let i = 0; i < lista.length; i++) {
                            let opt = document.createElement('option');
                            opt.setAttribute("value", lista[i]);
                            opt.innerHTML = lista[i];
                            if (lista[i] === value) {
                                opt.setAttribute("selected", "selected");
                            }
                            input.appendChild(opt);
                        }
                        break;
                    case "multi_array":
                        input = document.createElement("select");
                        input.setAttribute("multiple", "");
                        let ls = infos["arrays"][i];
                        console.log(ls);
                        for (let i = 0; i < ls.length; i++) {
                            let opt = document.createElement('option');
                            opt.setAttribute("value", ls[i]);
                            opt.innerHTML = ls[i];
                            if (value.includes(ls[i])) {
                                opt.setAttribute("selected", "true");
                            }
                            input.appendChild(opt);
                        }
                    default:
                        break;
                }
                
                input.setAttribute("name", key);
                
                form.appendChild(label);
                form.appendChild(document.createElement("br"));
                form.appendChild(input);
            }
        }
        
        let btn_mod = document.createElement("input");
        btn_mod.setAttribute("type", "submit");
        btn_mod.setAttribute("value", "Modificar");
        form.appendChild(btn_mod);
        
        let ind = document.createElement("input");
        ind.style.display= "none";
        ind.setAttribute("name", "mod");
        form.appendChild(ind);
        
        let id_ind = document.createElement("input");
        id_ind.style.display= "none";
        id_ind.setAttribute("type", "text");
        id_ind.setAttribute("name", "id");
        id_ind.setAttribute("value", id);
        form.appendChild(id_ind);
        
        let type_ind = document.createElement("input");
        type_ind.style.display= "none";
        type_ind.setAttribute("type", "text");
        type_ind.setAttribute("name", "tipo");
        type_ind.setAttribute("value", infos["tipo"]);
        form.appendChild(type_ind);
        
        div_cont.appendChild(form);
        div.appendChild(div_cont);
        
        document.body.appendChild(div);
    }

}

function search() {
    let nome = document.getElementById("busca_nome").value;
    //pla = document.forms.namedItem("busca_pla").innerHTML;
    //est = document.forms.namedItem("busca_est").innerHTML;
    //sist = document.forms.namedItem("busca_sist").innerHTML;
    //gal = document.forms.namedItem("busca_gal").innerHTML;
    //sat = document.forms.namedItem("busca_sat").innerHTML;
    let pla = true;
    let gal = false;
    let est = false;
    let sist = false;
    let sat = false;

    let infos = document.getElementById("lista-entidades");
    infos.parentNode.removeChild(infos);

    get_entidades(nome, {"planeta": pla, "estrela": est, "galaxia": gal, "satelite": sat, "sistema": sist});

    return false;
}

get_entidades("", {"planeta": true, "galaxia": true, "estrela": true, "satelite": true, "sistema": true});
