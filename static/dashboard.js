document.addEventListener('DOMContentLoaded', function() {
    // Club Filter Logic
    const clubFilter = document.getElementById('club-filter') || document.getElementById('club_filter'); // Check for both possible IDs
    if (clubFilter) {
        const eventCards = document.querySelectorAll('.event-card');

        clubFilter.addEventListener('change', function() {
            const selectedClub = clubFilter.value;
            eventCards.forEach(card => {
                if (selectedClub === 'all' || card.getAttribute('data-club') === selectedClub) {
                    card.style.display = 'block';
                } else {
                    card.style.display = 'none';
                }
            });
        });
    }

    // Register Button Logic
    const registerButtons = document.querySelectorAll('.register-button, .register-btn'); // Select both possible class names
    registerButtons.forEach(button => {
        button.addEventListener('click', function() {
            const eventId = this.getAttribute('data-event-id') || this.dataset.eventId; // Check for both possible attributes
            fetch(`/register_event/${eventId}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert('Successfully registered for the event!');
                    location.reload();
                } else {
                    alert('Failed to register for the event.');
                }
            });
        });
    });

    // Unregister Button Logic
    const unregisterButtons = document.querySelectorAll('.unregister-btn');
    unregisterButtons.forEach(button => {
        button.addEventListener('click', function() {
            const eventId = this.dataset.eventId;
            fetch(`/unregister_event/${eventId}`, {
                method: 'POST'
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert('Unregistered successfully!');
                    location.reload();
                } else {
                    alert('Unregistration failed.');
                }
            });
        });
    });
});
