

let tds = document.querySelectorAll('.detalhes')

var textbox = document.querySelector("#filtropapelcota")



textbox.addEventListener('input',()=>{
    tds.forEach((element)=>{
        element.style.display = "table-row"
    })
    filtrartabela(textbox.value)
})



function filtrartabela(base_string){


    tds.forEach(element1 => {

        let childs = element1.childNodes
        console.log(element1.parentNode)

        let teste = filtroteste(childs,base_string)

        if (teste) {
            // element1.style.display = "block"
        } else {
            element1.style.display = "none"
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
