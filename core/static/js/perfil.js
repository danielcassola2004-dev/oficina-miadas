document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('.perfil-form');

    if (form) {
        form.addEventListener('submit', function(e) {
            const nome = document.getElementById('nome').value;
            const email = document.getElementById('email').value;

            if (!nome || !email) {
                e.preventDefault();
                alert('Por favor, preencha os campos obrigatórios!');
            }
        });
    }

    console.log('✅ Perfil Carregado!');
});