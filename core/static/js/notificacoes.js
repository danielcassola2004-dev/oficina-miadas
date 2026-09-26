function showNotification(message, type="success", duration=3000) {

    const container = document.getElementById("notification-container");

    const notification = document.createElement("div");
    notification.classList.add("notification", type);

    notification.innerHTML = `
        <span>${message}</span>
        <button>&times;</button>
    `;

    container.appendChild(notification);

    // Botão fechar manual
    notification.querySelector("button").addEventListener("click", () => {
        removeNotification(notification);
    });

    // Auto remover
    setTimeout(() => {
        removeNotification(notification);
    }, duration);
}

function removeNotification(notification) {
    notification.style.animation = "fadeOut 0.4s ease forwards";
    setTimeout(() => {
        notification.remove();
    }, 400);
}
