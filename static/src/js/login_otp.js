document.addEventListener('DOMContentLoaded', function () {
    // Select elements
    var sendOtpButton = document.getElementById('sendOtpButton');
    var verifyOtpButton = document.getElementById('verifyOtpButton');
    var otpInput = document.getElementById('otp');
    var loginButton = document.getElementById('loginButton');
    var otpSection = document.getElementById('otpSection');
    var passwordSection = document.getElementById('passwordSection');
    var emailInput = document.getElementById('email');
    var loginForm = document.getElementById('loginForm');

    // Show OTP section when email is entered
    emailInput.addEventListener('input', function () {
        otpSection.style.display = emailInput.value ? 'block' : 'none';
        passwordSection.style.display = emailInput.value ? 'none' : 'block';
    });

    // Send OTP
    sendOtpButton.addEventListener('click', function () {
        var email = emailInput.value;
        if (email) {
            // Enable OTP input and verify button
            otpInput.disabled = false;
            verifyOtpButton.disabled = false;

            // Send OTP request to server
            fetch('/auction/login/request_otp', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    email: email
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert('OTP sent to your email.');
                } else {
                    alert('Failed to send OTP. ' + data.message);
                }
            })
            .catch(error => {
                console.error('Error occurred:', error); // Log the error for debugging
                alert('Error occurred while sending OTP: ' + error);
            });
        } else {
            alert('Please enter a valid email.');
        }
    });

    // Verify OTP
    verifyOtpButton.addEventListener('click', function () {
        var otp = otpInput.value;
        var email = emailInput.value;
        if (otp) {
            // Send OTP verification request to server
            fetch('/auction/login/verify_otp', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    email: email,
                    otp: otp
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // OTP verified, enable login button
                    loginButton.disabled = false;
                    alert('OTP Verified. You can now login.');
                } else {
                    alert('Invalid OTP.');
                }
            })
            .catch(error => {
                console.error('Error occurred:', error);
                alert('Error verifying OTP: ' + error);
            });
        } else {
            alert('Please enter the OTP.');
        }
    });

    // Handle login form submission
    loginForm.addEventListener('submit', function (event) {
        event.preventDefault();

        // Submit login form only if OTP is verified or password is entered
        if (otpInput.disabled === false && otpInput.value) {
            // Proceed with login
            loginForm.submit();
        } else if (passwordSection.style.display === 'block' && document.getElementById('password').value) {
            // Proceed with login using password
            loginForm.submit();
        } else {
            alert('Please complete the login process.');
        }
    });
});
