

let cards = document.querySelectorAll('.card')

var textbox = document.querySelector("#busca_ativos")



textbox.addEventListener('input',()=>{
    cards.forEach((element)=>{
        element.style.display = "block"
    })
    filtrartabela(textbox.value)
})



function filtrartabela(base_string){


    cards.forEach(element1 => {

        let childs = element1.childNodes
        console.log(element1.parentNode)

        let teste = filtroteste(childs,base_string)

        if (teste) {
            // element1.style.display = "block"
        } else {
            element1.style.display = "none";
        }

    })





}



function filtroteste(elementos , base_string){

    let teste = false

    elementos.forEach((element)=>{

        if( element.textContent.toLowerCase().includes(base_string.toLowerCase())){
            teste = true
        } else {

        }

        // console.log(element.textContent)
    })

    return teste






}
