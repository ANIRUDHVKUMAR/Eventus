document.addEventListener('DOMContentLoaded', function() {
    const addEventLink = document.getElementById('add-event-link');
    const modifyEventLink = document.getElementById('modify-event-link');
    const removeEventLink = document.getElementById('remove-event-link');
    const pastEventsLink = document.getElementById('past-events-link');

    const addEventForm = document.getElementById('add-event-form');
    const modifyEventForm = document.getElementById('modify-event-form');
    const removeEventForm = document.getElementById('remove-event-form');
    const pastEventsContainer = document.getElementById('past-events-container');

    addEventLink.addEventListener('click', function(event) {
        event.preventDefault();
        addEventForm.style.display = 'block';
        modifyEventForm.style.display = 'none';
        removeEventForm.style.display = 'none';
        pastEventsContainer.style.display = 'none';
    });

    modifyEventLink.addEventListener('click', function(event) {
        event.preventDefault();
        addEventForm.style.display = 'none';
        modifyEventForm.style.display = 'block';
        removeEventForm.style.display = 'none';
        pastEventsContainer.style.display = 'none';
    });

    removeEventLink.addEventListener('click', function(event) {
        event.preventDefault();
        addEventForm.style.display = 'none';
        modifyEventForm.style.display = 'none';
        removeEventForm.style.display = 'block';
        pastEventsContainer.style.display = 'none';
    });

    pastEventsLink.addEventListener('click', function(event) {
        event.preventDefault();
        addEventForm.style.display = 'none';
        modifyEventForm.style.display = 'none';
        removeEventForm.style.display = 'none';
        pastEventsContainer.style.display = 'block';
    });
});
