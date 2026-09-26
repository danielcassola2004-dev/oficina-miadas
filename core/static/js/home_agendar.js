// HOME_AGENDAR.JS - Validações e funcionalidades do formulário

document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('.agendar-form');
    const dataInput = document.getElementById('data');
    const horaInput = document.getElementById('hora');
    const telefoneInput = document.getElementById('telefone');

    // Definir data mínima como hoje
    const today = new Date().toISOString().split('T')[0];
    dataInput.setAttribute('min', today);

    // Validar telefone (apenas números)
    telefoneInput.addEventListener('input', function() {
        this.value = this.value.replace(/[^0-9+]/g, '');
    });

    // Validar horário (não permitir horas antes das 08:00 ou depois das 18:00)
    horaInput.addEventListener('change', function() {
        const hora = this.value.split(':')[0];
        if (hora < 8 || hora >= 18) {
            alert('Por favor, escolha um horário entre 08:00 e 18:00');
            this.value = '';
        }
    });

    // Validar formulário antes de enviar
    form.addEventListener('submit', function(e) {
        const servico = document.getElementById('servico').value;
        const data = document.getElementById('data').value;
        const hora = document.getElementById('hora').value;

        if (!servico || !data || !hora) {
            e.preventDefault();
            alert('Por favor, preencha todos os campos obrigatórios');
        }
    });
});