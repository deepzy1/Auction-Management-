// Auction Countdown Logic
document.addEventListener("DOMContentLoaded", function () {
    // Find all countdown elements
    const countdownElements = document.querySelectorAll("[data-auction-start]");

    countdownElements.forEach(function (element) {
        // Parse the start date from the `data-auction-start` attribute
        const startDatestr = new Date(element.getAttribute("data-auction-start"));
        const startDate= new Date(startDatestr+"UTC")

        // Function to update the countdown
        function updateCountdown() {
            const now = new Date();
            const diff = startDate - now;

            if (diff >=0) {
                const days = Math.floor(diff / (1000 * 60 * 60 * 24));
                const hours = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
                const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
                const seconds = Math.floor((diff % (1000 * 60)) / 1000);

                // Format the time as days:hours:minutes:seconds
                element.innerHTML = `${days}d:${String(hours).padStart(2, '0')}h:${String(minutes).padStart(2, '0')}m:${String(seconds).padStart(2, '0')}s`;
            }
            else {
                element.innerHTML = "Auction ended";
            }
        }

        // Start the countdown and update every second
        updateCountdown();
        setInterval(updateCountdown, 1000);
    });
});
