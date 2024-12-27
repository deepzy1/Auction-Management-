document.addEventListener('DOMContentLoaded', function () {
    console.log('DOMContentLoaded event triggered');
    var sendOtpButton = document.getElementById('sendOtpButton');
    console.log("Server response:");

    if (sendOtpButton) {
        sendOtpButton.addEventListener('click', function () {
            var email = document.getElementById('email').value;
            console.log('Email entered:', email);

            if (!email) {
                alert('Please enter your email first.');
                return;
            }

            fetch('/auction/register/send_otp', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ email: email })
            })
            .then(response => response.json()) // Parse the response as JSON
            .then(data => {
                console.log('Server response:', data); // Log the response to check its structure

                if (data.result.success) {
                    alert('OTP has been sent to your email.');
                    document.getElementById('otp').disabled = false; // Enable OTP input field
                    document.getElementById('verifyOtpButton').disabled = false; // Enable Verify OTP button
                    document.getElementById('sendOtpButton').disabled = true; // Disable Send OTP button
                } else {
                    alert(data.result.message || 'Something went wrong. Try again.');
                }
            })
            .catch(error => {
                console.error('Error occurred:', error); // Log the error for debugging
                alert('Error: ' + error);
            });
        });
    } else {
        console.error('sendOtpButton element not found.');
    }
});