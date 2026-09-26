document.addEventListener(
"DOMContentLoaded",
()=>{


const modal =
document.getElementById(
"clienteModal"
);


const info =
document.getElementById(
"clienteInfo"
);



/* ABRIR MODAL */

document.querySelectorAll(
".view-client"
)
.forEach(btn=>{


btn.addEventListener(
"click",
()=>{


let id = btn.dataset.id;



fetch(
`/admin/clientes/detalhes/${id}/`
)


.then(res=>res.json())


.then(data=>{


let html = `


<div class="cliente-detalhes">


<h3>
${data.nome}
</h3>


<p>
<strong>Email:</strong>
${data.email}
</p>


<p>
<strong>Telefone:</strong>
${data.telefone}
</p>


<p>
<strong>Registo:</strong>
${data.data_registo}
</p>


<p>
<strong>Total de agendamentos:</strong>
${data.total_agendamentos}
</p>



<h4>
Agendamentos
</h4>



`;



data.agendamentos.forEach(ag=>{


html += `

<div class="agendamento-item">


<p>
${ag.servico}
</p>


<span>
${ag.data} - ${ag.hora}
</span>


<span>
${ag.status}
</span>


</div>

`;


});



html += "</div>";



info.innerHTML = html;


modal.style.display="flex";


});


});


});






/* FECHAR MODAL */


document.querySelector(
".close-modal"
)
.onclick=()=>{

modal.style.display="none";

};





/* REMOVER CLIENTE */


document.querySelectorAll(
".delete-client"
)
.forEach(btn=>{


btn.onclick=()=>{


let id =
btn.dataset.id;



if(confirm(
"Tem certeza que deseja remover este cliente?"
)){



fetch(
`/admin/clientes/remover/${id}/`,
{

method:"POST",

headers:{

"X-CSRFToken":
getCookie("csrftoken")

}

}

)


.then(
res=>res.json()
)


.then(data=>{


alert(data.mensagem);


location.reload();


});


}


}



});





});





function getCookie(name){

let cookieValue=null;


if(document.cookie){

let cookies =
document.cookie.split(";");


cookies.forEach(cookie=>{


cookie=cookie.trim();


if(cookie.startsWith(name+"=")){


cookieValue=
decodeURIComponent(
cookie.substring(
name.length+1
)
);


}


});


}


return cookieValue;

}