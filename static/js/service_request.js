document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('serviceRequestForm');
    const messagePopup = document.getElementById('messagePopup');
    const messageText = messagePopup.querySelector('.message-text');

    // Function to show message popup
    function showMessagePopup(message, isSuccess) {
        messageText.textContent = message;
        messagePopup.className = `message-popup ${isSuccess ? 'success' : 'error'}`;
        messagePopup.style.display = 'block';
        
        // Auto hide after 5 seconds
        setTimeout(() => {
            closeMessagePopup();
        }, 5000);
    }

    // Function to close message popup
    window.closeMessagePopup = function() {
        messagePopup.style.display = 'none';
    }

    // Handle form submission
    if (form) {
        form.addEventListener('submit', function(e) {
            e.preventDefault();

            // Show loading state
            const submitBtn = form.querySelector('button[type="submit"]');
            const originalText = submitBtn.textContent;
            submitBtn.textContent = 'Submitting...';
            submitBtn.disabled = true;

            fetch(form.action, {
                method: 'POST',
                body: new FormData(form),
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                if (data.success) {
                    showMessagePopup(data.message, true);
                    form.reset();
                } else {
                    showMessagePopup(data.message || 'An error occurred. Please try again.', false);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                // Fallback to regular form submission
                showMessagePopup('Submitting form...', true);
                form.submit();
            })
            .finally(() => {
                // Restore button state
                submitBtn.textContent = originalText;
                submitBtn.disabled = false;
            });
        });
    }

    // Check for messages on page load
    const messages = document.querySelectorAll('.messages .alert');
    if (messages.length > 0) {
        const firstMessage = messages[0];
        const isSuccess = firstMessage.classList.contains('alert-success');
        showMessagePopup(firstMessage.dataset.message, isSuccess);
    }
});
