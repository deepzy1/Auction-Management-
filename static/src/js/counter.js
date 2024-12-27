document.addEventListener("DOMContentLoaded", function () {
    function updateCountdown() {
        const countdownElements = document.querySelectorAll('.countdown-timer');

        countdownElements.forEach(function (element) {
            // Get the auction end date from the data attribute
            const auctionEndDateStr = element.getAttribute('data-auction-end');
            
            // Parse the auction end date string into a Date object
            const auctionEndDate = new Date(auctionEndDateStr); // This is in UTC

            // Convert auctionEndDate to local time
            const auctionEndDateLocal = new Date(auctionEndDate.getTime() - auctionEndDate.getTimezoneOffset() * 60000);
            
            // Get the current time (local time)
            const currentTime = new Date();  // Local time

            console.log("Auction End Date (Local):", auctionEndDateLocal.toString());
            console.log("Current Time (Local):", currentTime.toString());

            // Calculate the remaining time in milliseconds
            const remainingTimeInMilliseconds = auctionEndDateLocal - currentTime;

            console.log("Remaining Time in Milliseconds:", remainingTimeInMilliseconds);

            const oneHourInMilliseconds = 3600 * 1000;  // 1 hour in milliseconds

            const hurryTextElement = element.querySelector('.hurry-text');
            const countdownElement = element.querySelector('.countdown-time');

            // Check if the auction is running and if it will end in less than 1 hour
            if (remainingTimeInMilliseconds > 0 && remainingTimeInMilliseconds <= oneHourInMilliseconds) {
                // Convert milliseconds into hours, minutes, and seconds
                const remainingTimeInSeconds = remainingTimeInMilliseconds / 1000;  // Convert to seconds
                const hours = Math.floor(remainingTimeInSeconds / 3600);
                const minutes = Math.floor((remainingTimeInSeconds % 3600) / 60);
                const seconds = Math.floor(remainingTimeInSeconds % 60);

                const countdownText = `${hours}h ${minutes}m ${seconds}s`;
                countdownElement.textContent = countdownText;
                element.style.display = 'block';  // Show countdown
                hurryTextElement.style.display = 'inline';  // Show "Hurry Up!" in red

                console.log("Countdown Text:", countdownText);
            } else {
                // Hide countdown if more than 1 hour or already ended
                element.style.display = 'none';
                hurryTextElement.style.display = 'none';  // Hide "Hurry Up!" text
                console.log("Countdown hidden, auction ended or more than 1 hour left.");
            }
        });
    }

    // Initial call to update countdown
    updateCountdown();

    // Optionally set an interval to update the countdown every second
    setInterval(updateCountdown, 1000);  // Update every second
});
