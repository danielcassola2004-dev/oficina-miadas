document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('.agendar-form');
    const dataInput = document.getElementById('data');
    const horaInput = document.getElementById('hora');

    // Set minimum date to today
    const today = new Date().toISOString().split('T')[0];
    dataInput.setAttribute('min', today);

    // Form validation
    form.addEventListener('submit', function(e) {
        const servico = document.getElementById('servico').value;
        const data = dataInput.value;
        const hora = horaInput.value;

        if (!servico || !data || !hora) {
            e.preventDefault();
            alert('Por favor, preencha todos os campos obrigatórios!');
        }
    });

    console.log('✅ Agendar Carregado!');
});