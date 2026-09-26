document.addEventListener('DOMContentLoaded', function() {
    // ============================================
    // CALCULAR STATS CORRETAMENTE
    // ============================================

    const rows = document.querySelectorAll('.appointments-table tbody tr');
    let total = 0;
    let confirmados = 0;
    let pendentes = 0;
    let cancelados = 0;

    rows.forEach(row => {
        const status = row.getAttribute('data-status');
        total++;

        if (status === 'confirmado') {
            confirmados++;
        } else if (status === 'pendente') {
            pendentes++;
        } else if (status === 'cancelado') {
            cancelados++;
        }
    });

    console.log('📊 Stats Calculados:');
    console.log('Total:', total);
    console.log('Confirmados:', confirmados);
    console.log('Pendentes:', pendentes);
    console.log('Cancelados:', cancelados);

    console.log('✅ Home Cliente Premium Carregado!');
});