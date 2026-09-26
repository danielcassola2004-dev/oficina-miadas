/* 
    Oficina Miadas - Modern JS for TCC
    Author: Manus AI
    Focus: Interactivity, Smooth Scrolling, Modal Logic
    Otimizado para serviços dinâmicos
*/

document.addEventListener('DOMContentLoaded', () => {
    // Comentário: Elementos do DOM
    const header = document.getElementById('header');
    const menuToggle = document.getElementById('menu-toggle');
    const nav = document.getElementById('nav');
    const modalOverlay = document.getElementById('modal-overlay');
    const modalClose = document.getElementById('modal-close');
    const modalImg = document.getElementById('modal-img');
    const modalTitle = document.getElementById('modal-title');
    const modalText = document.getElementById('modal-text');
    const modalBtns = document.querySelectorAll('.btn-modal');

    // ============================================================
    // 1. EFEITO DE SCROLL NO HEADER
    // ============================================================
    
    /* Comentário: Adiciona classe 'scrolled' ao header quando scroll > 50px */
    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            header.classList.add('scrolled');
        } else {
            header.classList.remove('scrolled');
        }
    });

    // ============================================================
    // 2. MENU MOBILE TOGGLE
    // ============================================================
    
    /* Comentário: Abre/fecha menu mobile e anima o ícone hambúrguer */
    menuToggle.addEventListener('click', () => {
        nav.classList.toggle('active');
        menuToggle.classList.toggle('active');
        
        // Comentário: Animação do ícone hambúrguer
        const bars = menuToggle.querySelectorAll('.bar');
        if (nav.classList.contains('active')) {
            bars[0].style.transform = 'rotate(-45deg) translate(-5px, 6px)';
            bars[1].style.opacity = '0';
            bars[2].style.transform = 'rotate(45deg) translate(-5px, -6px)';
        } else {
            bars[0].style.transform = 'none';
            bars[1].style.opacity = '1';
            bars[2].style.transform = 'none';
        }
    });

    // Comentário: Fechar menu ao clicar em um link (Mobile)
    const navLinks = document.querySelectorAll('.nav-link');
    navLinks.forEach(link => {
        link.addEventListener('click', () => {
            nav.classList.remove('active');
            // Comentário: Resetar ícone hambúrguer
            const bars = menuToggle.querySelectorAll('.bar');
            bars[0].style.transform = 'none';
            bars[1].style.opacity = '1';
            bars[2].style.transform = 'none';
        });
    });

    // ============================================================
    // 3. LÓGICA DO MODAL PARA PUBLICIDADES
    // ============================================================
    
    /* Comentário: Abrir modal ao clicar em "Saber Mais" */
    modalBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const img = btn.getAttribute('data-img');
            const title = btn.getAttribute('data-title');
            const text = btn.getAttribute('data-text');

            // Comentário: Preencher conteúdo do modal
            modalImg.src = img;
            modalTitle.innerText = title;
            modalText.innerText = text;

            // Comentário: Mostrar modal
            modalOverlay.classList.add('active');
            document.body.style.overflow = 'hidden'; // Prevenir scroll
        });
    });

    // Comentário: Função para fechar modal
    const closeModal = () => {
        modalOverlay.classList.remove('active');
        document.body.style.overflow = 'auto';
    };

    // Comentário: Fechar ao clicar no X
    modalClose.addEventListener('click', closeModal);
    
    // Comentário: Fechar ao clicar fora do conteúdo do modal
    modalOverlay.addEventListener('click', (e) => {
        if (e.target === modalOverlay) {
            closeModal();
        }
    });

    // Comentário: Fechar modal ao pressionar ESC
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            closeModal();
        }
    });

    // ============================================================
    // 4. SMOOTH SCROLL PARA LINKS INTERNOS
    // ============================================================
    
    /* Comentário: Smooth scroll para âncoras internas */
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                const headerOffset = 80;
                const elementPosition = target.getBoundingClientRect().top;
                const offsetPosition = elementPosition + window.pageYOffset - headerOffset;

                window.scrollTo({
                    top: offsetPosition,
                    behavior: 'smooth'
                });
            }
        });
    });

    // ============================================================
    // 5. ANIMAÇÕES DE SERVIÇOS DINÂMICOS
    // ============================================================
    
    /* Comentário: Adicionar efeitos aos cards de serviço */
    const serviceCards = document.querySelectorAll('.service-card');
    
    serviceCards.forEach((card, index) => {
        // Comentário: Efeito de entrada escalonada
        card.style.animationDelay = `${index * 0.1}s`;
        
        // Comentário: Adicionar ripple effect ao clicar no botão
        const btnCircle = card.querySelector('.btn-circle');
        if (btnCircle) {
            btnCircle.addEventListener('click', (e) => {
                const ripple = document.createElement('span');
                ripple.style.position = 'absolute';
                ripple.style.borderRadius = '50%';
                ripple.style.background = 'rgba(255, 255, 255, 0.6)';
                ripple.style.width = '20px';
                ripple.style.height = '20px';
                ripple.style.animation = 'ripple 0.6s ease-out';
                
                const rect = btnCircle.getBoundingClientRect();
                const size = Math.max(rect.width, rect.height);
                const x = e.clientX - rect.left - size / 2;
                const y = e.clientY - rect.top - size / 2;
                
                ripple.style.left = x + 'px';
                ripple.style.top = y + 'px';
                ripple.style.width = size + 'px';
                ripple.style.height = size + 'px';
                
                btnCircle.appendChild(ripple);
                
                setTimeout(() => ripple.remove(), 600);
            });
        }
    });

    // ============================================================
    // 6. LAZY LOADING PARA IMAGENS
    // ============================================================
    
    /* Comentário: Lazy loading de imagens para melhor performance */
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    if (img.dataset.src) {
                        img.src = img.dataset.src;
                        img.removeAttribute('data-src');
                    }
                    observer.unobserve(img);
                }
            });
        });

        document.querySelectorAll('img[data-src]').forEach(img => {
            imageObserver.observe(img);
        });
    }

    // ============================================================
    // 7. CONTADOR DE SERVIÇOS
    // ============================================================
    
    /* Comentário: Contar e exibir número de serviços disponíveis */
    const serviceCount = document.querySelectorAll('.service-card').length;
    console.log(`Total de serviços disponíveis: ${serviceCount}`);

    // ============================================================
    // 8. VALIDAÇÃO DE FORMULÁRIOS (Se houver)
    // ============================================================
    
    /* Comentário: Adicionar validação básica a formulários */
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', (e) => {
            const inputs = form.querySelectorAll('input[required]');
            let isValid = true;
            
            inputs.forEach(input => {
                if (!input.value.trim()) {
                    isValid = false;
                    input.style.borderColor = '#ff453a';
                } else {
                    input.style.borderColor = '';
                }
            });
            
            if (!isValid) {
                e.preventDefault();
                console.warn('Formulário inválido');
            }
        });
    });
});

// ============================================================
// ANIMAÇÃO RIPPLE (CSS)
// ============================================================

/* Comentário: Adicionar animação ripple ao CSS dinamicamente */
const style = document.createElement('style');
style.textContent = `
    @keyframes ripple {
        0% {
            transform: scale(0);
            opacity: 1;
        }
        100% {
            transform: scale(4);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);
