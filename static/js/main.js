// Particle.js Configuration
particlesJS('particles-js', {
    particles: {
        number: {
            value: 80,
            density: {
                enable: true,
                value_area: 800
            }
        },
        color: {
            value: '#667eea'
        },
        shape: {
            type: 'circle',
            stroke: {
                width: 0,
                color: '#000000'
            }
        },
        opacity: {
            value: 0.5,
            random: false,
            anim: {
                enable: false,
                speed: 1,
                opacity_min: 0.1,
                sync: false
            }
        },
        size: {
            value: 3,
            random: true,
            anim: {
                enable: false,
                speed: 40,
                size_min: 0.1,
                sync: false
            }
        },
        line_linked: {
            enable: true,
            distance: 150,
            color: '#667eea',
            opacity: 0.4,
            width: 1
        },
        move: {
            enable: true,
            speed: 2,
            direction: 'none',
            random: false,
            straight: false,
            out_mode: 'out',
            bounce: false,
            attract: {
                enable: false,
                rotateX: 600,
                rotateY: 1200
            }
        }
    },
    interactivity: {
        detect_on: 'canvas',
        events: {
            onhover: {
                enable: true,
                mode: 'repulse'
            },
            onclick: {
                enable: true,
                mode: 'push'
            },
            resize: true
        },
        modes: {
            grab: {
                distance: 400,
                line_linked: {
                    opacity: 1
                }
            },
            bubble: {
                distance: 400,
                size: 40,
                duration: 2,
                opacity: 8,
                speed: 3
            },
            repulse: {
                distance: 200,
                duration: 0.4
            },
            push: {
                particles_nb: 4
            },
            remove: {
                particles_nb: 2
            }
        }
    },
    retina_detect: true
});

// Your existing JavaScript code
document.addEventListener('DOMContentLoaded', function() {
    const refreshBtn = document.getElementById('refreshBtn');

    if (refreshBtn) {
        refreshBtn.addEventListener('click', function() {
            const cryptoId = this.getAttribute('data-crypto-id');
            refreshPrice(cryptoId);
        });
    }

    function refreshPrice(cryptoId) {
        const refreshBtn = document.getElementById('refreshBtn');
        const originalText = refreshBtn.innerHTML;

        // Show loading state
        refreshBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-1"></i>Loading...';
        refreshBtn.disabled = true;

        // Get CSRF token
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

        fetch(`/api/refresh/${cryptoId}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken,
            },
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Update the price display
                document.getElementById('currentPrice').textContent = `$${parseFloat(data.data.price).toFixed(8)}`;

                // Update price change
                const priceChangeElement = document.getElementById('priceChange');
                const priceChange = parseFloat(data.data.price_change_24h);
                priceChangeElement.textContent = `${priceChange.toFixed(2)}%`;
                priceChangeElement.className = priceChange >= 0 ? 'text-success' : 'text-danger';

                // Update market cap
                const marketCapElement = document.getElementById('marketCap');
                if (data.data.market_cap) {
                    marketCapElement.textContent = `${parseInt(data.data.market_cap).toLocaleString()}`;
                }

                // Update volume
                const volumeElement = document.getElementById('volume24h');
                if (data.data.volume_24h) {
                    volumeElement.textContent = `${parseInt(data.data.volume_24h).toLocaleString()}`;
                }

                // Show success message
                showAlert('Price updated successfully!', 'success');
            } else {
                showAlert('Failed to update price. Please try again.', 'danger');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showAlert('An error occurred while updating the price.', 'danger');
        })
        .finally(() => {
            // Reset button state
            refreshBtn.innerHTML = originalText;
            refreshBtn.disabled = false;
        });
    }

    function showAlert(message, type) {
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
        alertDiv.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;

        const container = document.querySelector('.container');
        container.insertBefore(alertDiv, container.firstChild);

        // Auto dismiss after 3 seconds
        setTimeout(() => {
            alertDiv.remove();
        }, 3000);
    }
});