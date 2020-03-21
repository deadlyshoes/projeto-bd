async function print_infos(id) {
    data = id;
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
        div.className = "infos";
        
        for (var key in infos) {
            let p = document.createElement("p");
            p.innerHTML = key.concat(": ".concat(infos[key]));
            
            div.appendChild(p);
        }
        
        document.body.appendChild(div);
    }
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
            div.id = obj["id"];
            div.onclick = function() {print_infos(this.id);};
            div.style.cursor = "pointer";
        
            let nome = document.createElement("span"); 
            nome.innerHTML = "Nome: ".concat(obj["Nome"]);
            div.appendChild(nome);
            
            div.appendChild(document.createElement("br"));
            
            let id = document.createElement("span");
            id.innerHTML = "#".concat(obj["id"]);
            div.appendChild(id);
    
            parentDiv.appendChild(div);
        }
        
        document.body.appendChild(parentDiv);
    }
}

get_entidades();
