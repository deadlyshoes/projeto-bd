async function get_entidades() {
    let response = fetch("/entidades");
    
    if (response.ok) {
        let entidades = await response.json();
        for (let i = 0; i < entidades.length(); i++) {
            let div = document.createElement("div");
            div.className = "mini-cabecalho";
            div.appendChild("test");
            parentDiv.appendChild(div);
        }
    }
}
