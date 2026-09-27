/* ==========================================================================
   CodeAlpha Simple E-commerce Store Client JavaScript
   ========================================================================== */

document.addEventListener('DOMContentLoaded', () => {
    // 1. Auto dismiss alert messages after 4 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
            alert.style.opacity = '0';
            alert.style.transform = 'translateY(-10px)';
            setTimeout(() => alert.remove(), 500);
        }, 4000);
    });

    // 2. Alert close buttons
    const closeButtons = document.querySelectorAll('.alert-close');
    closeButtons.forEach(btn => {
        btn.addEventListener('click', (e) => {
            const alert = e.target.closest('.alert');
            if (alert) alert.remove();
        });
    });

    // 3. Quantity Stepper Controls (if any)
    const qtyInputs = document.querySelectorAll('.quantity-input');
    qtyInputs.forEach(input => {
        input.addEventListener('change', () => {
            const min = parseInt(input.getAttribute('min') || '1');
            const max = parseInt(input.getAttribute('max') || '999');
            let val = parseInt(input.value);
            if (isNaN(val) || val < min) val = min;
            if (val > max) val = max;
            input.value = val;
        });
    });
});

/**
 * Toast Notification Helper
 */
function showToast(message, type = 'success') {
    let container = document.querySelector('.messages-container');
    if (!container) {
        container = document.createElement('div');
        container.className = 'messages-container';
        document.body.insertBefore(container, document.querySelector('main'));
    }

    const alert = document.createElement('div');
    alert.className = `alert alert-${type}`;
    alert.innerHTML = `
        <span>${message}</span>
        <button class="alert-close" onclick="this.parentElement.remove()">&times;</button>
    `;
    container.appendChild(alert);

    setTimeout(() => {
        alert.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
        alert.style.opacity = '0';
        alert.style.transform = 'translateY(-10px)';
        setTimeout(() => alert.remove(), 500);
    }, 3500);
}

/**
 * Async Add to Cart helper
 */
function addToCart(productId, quantity = 1) {
    const url = `/cart/add/${productId}/`;
    const csrfToken = getCookie('csrftoken');

    const formData = new FormData();
    formData.append('quantity', quantity);

    fetch(url, {
        method: 'POST',
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': csrfToken
        },
        body: formData
    })
    .then(response => {
        if (!response.ok) {
            return response.json().then(data => { throw new Error(data.message || 'Error adding to cart'); });
        }
        return response.json();
    })
    .then(data => {
        // Update badge count in header
        const badge = document.querySelector('.badge-count');
        if (badge) {
            badge.textContent = data.cart_count;
        } else {
            const cartLink = document.querySelector('.cart-badge-link');
            if (cartLink) {
                const newBadge = document.createElement('span');
                newBadge.className = 'badge-count';
                newBadge.textContent = data.cart_count;
                cartLink.appendChild(newBadge);
            }
        }
        showToast(data.message || 'Item added to cart!', 'success');
    })
    .catch(err => {
        showToast(err.message || 'Could not add product to cart', 'error');
    });
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
