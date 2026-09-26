document.addEventListener("DOMContentLoaded", function () {


    // ==============================
    // VERIFICAR SE EXISTEM DADOS
    // ==============================

    if (typeof dadosGraficos === "undefined") {

        console.error(
            "Dados dos gráficos não encontrados."
        );

        return;

    }



    // ==============================
    // GRÁFICO STATUS
    // ==============================


    const statusCanvas = document.getElementById(
        "chartStatus"
    );


    if(statusCanvas){

        new Chart(statusCanvas, {

            type: "doughnut",

            data: {

                labels: dadosGraficos.status.labels,

                datasets: [

                    {

                        label: "Agendamentos",

                        data: dadosGraficos.status.valores

                    }

                ]

            },

            options: {

                responsive:true,

                maintainAspectRatio:false

            }

        });


    }







    // ==============================
    // GRÁFICO RECEITA
    // ==============================


    const receitaCanvas = document.getElementById(
        "chartReceita"
    );


    if(receitaCanvas){


        new Chart(receitaCanvas, {


            type:"bar",


            data:{


                labels:dadosGraficos.receita.labels,


                datasets:[

                    {

                        label:"Receita (Kz)",

                        data:dadosGraficos.receita.valores

                    }

                ]


            },


            options:{


                responsive:true,


                maintainAspectRatio:false


            }


        });


    }









    // ==============================
    // GRÁFICO TENDÊNCIA
    // ==============================


    const tendenciaCanvas = document.getElementById(
        "chartTendencia"
    );



    if(tendenciaCanvas){


        new Chart(tendenciaCanvas,{


            type:"line",



            data:{


                labels:dadosGraficos.tendencia.labels,


                datasets:[

                    {

                    label:"Agendamentos",

                    data:dadosGraficos.tendencia.valores,

                    tension:0.4

                    }

                ]

            },



            options:{


                responsive:true,

                maintainAspectRatio:false


            }


        });



    }









    // ==============================
    // GRÁFICO COMPARECIMENTO
    // ==============================



    const compareCanvas = document.getElementById(
        "chartComparecimento"
    );



    if(compareCanvas){


        new Chart(compareCanvas,{


            type:"pie",



            data:{


                labels:dadosGraficos.comparecimento.labels,


                datasets:[


                    {

                    data:dadosGraficos.comparecimento.valores


                    }


                ]


            },


            options:{


                responsive:true,


                maintainAspectRatio:false


            }



        });



    }









    // ==============================
    // GRÁFICO MÉTODOS PAGAMENTO
    // ==============================



    const metodosCanvas = document.getElementById(
        "chartMetodos"
    );



    if(metodosCanvas){


        new Chart(metodosCanvas,{


            type:"bar",



            data:{


                labels:dadosGraficos.metodos.labels,


                datasets:[


                    {

                    label:"Quantidade",

                    data:dadosGraficos.metodos.valores


                    }


                ]


            },



            options:{


                responsive:true,


                maintainAspectRatio:false


            }



        });



    }




});





// ==============================
// FILTROS DE DATA
// ==============================


function aplicarFiltros(){


    let inicio = document.getElementById(
        "dataInicio"
    ).value;



    let fim = document.getElementById(
        "dataFim"
    ).value;



    if(!inicio || !fim){


        alert(
            "Selecione as duas datas."
        );


        return;


    }



    window.location.href =
        "?inicio=" + inicio +
        "&fim=" + fim;


}