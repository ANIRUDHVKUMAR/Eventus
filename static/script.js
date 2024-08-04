document.addEventListener('DOMContentLoaded', function () {
    const eventusTitle = document.getElementById('eventus-title');
    const loginContainer = document.getElementById('login-container');
    const signupContainer = document.getElementById('signup-container');
    const clubAdminLoginContainer = document.getElementById('club-admin-login-container');
    const signupBtn = document.getElementById('signup-btn');
    const clubAdminLoginBtn = document.getElementById('club-admin-login-btn');
    const backToLoginBtn = document.getElementById('back-to-login');
    const backToLoginFromClubAdminBtn = document.getElementById('back-to-login-from-club-admin');

    // Initial display of Eventus title
    setTimeout(() => {
        eventusTitle.style.opacity = '0'; // Fade out title
        eventusTitle.style.transition = 'opacity 2s ease-in-out';

        setTimeout(() => {
            eventusTitle.style.display = 'none'; // Hide title
            loginContainer.style.display = 'block'; // Show login container
            loginContainer.style.opacity = '1';
            loginContainer.style.transition = 'opacity 1s ease-in-out';
        }, 2000); // Time to fade out title
    }, 0);

    // Switch to signup container
    signupBtn.addEventListener('click', () => {
        loginContainer.style.display = 'none';
        signupContainer.style.display = 'block';
        signupContainer.style.opacity = '1';
    });

    // Switch back to login container
    backToLoginBtn.addEventListener('click', () => {
        signupContainer.style.display = 'none';
        loginContainer.style.display = 'block';
        loginContainer.style.opacity = '1';
    });

    // Switch to club admin login container
    clubAdminLoginBtn.addEventListener('click', () => {
        loginContainer.style.display = 'none';
        clubAdminLoginContainer.style.display = 'block';
        clubAdminLoginContainer.style.opacity = '1';
    });

    // Switch back to login container from club admin login
    backToLoginFromClubAdminBtn.addEventListener('click', () => {
        clubAdminLoginContainer.style.display = 'none';
        loginContainer.style.display = 'block';
        loginContainer.style.opacity = '1';
    });
});
