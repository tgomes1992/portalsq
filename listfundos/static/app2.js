

ativo = document.querySelector("#ativo")


ativos = document.querySelectorAll(".ativos")


botao = document.querySelector("#botao")


// ativos.forEach(element => {
//     console.log(element.innerHTML)
// });


function filtrarativos (filterstring ) {

    console.log(filterstring)


    let findstring  = filterstring.toLowerCase()


    ativos.forEach(element => {   
        if ( ! element.getAttribute('data-id').toLowerCase().includes(findstring)) {
        
            element.style.display =  'none';
        } else {
            element.style.display =  "block" ;
        }
    });
}


ativo.addEventListener( 'input' , (e)=>{

    console.log(ativo)
    filtrarativos(ativo.value)


})



