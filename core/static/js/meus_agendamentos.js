document.addEventListener('DOMContentLoaded', function() {
    const filterBtns = document.querySelectorAll('.filter-btn');
    const agendamentoCards = document.querySelectorAll('.agendamento-card');

    filterBtns.forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            
            filterBtns.forEach(b => b.classList.remove('active'));
            this.classList.add('active');

            const status = this.getAttribute('href').split('=')[1];
            
            agendamentoCards.forEach(card => {
                if (!status || card.getAttribute('data-status') === status) {
                    card.style.display = 'block';
                    card.style.animation = 'slideUp 0.5s ease';
                } else {
                    card.style.display = 'none';
                }
            });
        });
    });

    console.log('✅ Meus Agendamentos Carregado!');
});