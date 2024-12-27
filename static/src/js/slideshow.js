document.addEventListener("DOMContentLoaded", function () {
    console.log("Custom Slideshow Page Loaded");

    const slides = document.querySelectorAll(".slide");
    const prevButton = document.getElementById("prevButton");
    const nextButton = document.getElementById("nextButton");
    const slideshowContainer = document.getElementById("property-slideshow");
    let currentIndex = 0;

    function showSlide(index) {
        // Hide all slides
        slides.forEach(slide => slide.classList.remove("active"));
        // Show the slide at the given index
        slides[index].classList.add("active");
    }

    function showNextSlide() {
        currentIndex = (currentIndex + 1) % slides.length; // Loop back to the first slide
        showSlide(currentIndex);
    }

    function showPrevSlide() {
        currentIndex = (currentIndex - 1 + slides.length) % slides.length; // Loop to the last slide
        showSlide(currentIndex);
    }

    function hideArrows() {
        prevButton.style.display = "none";
        nextButton.style.display = "none";
    }

    function showArrows() {
        prevButton.style.display = "block";
        nextButton.style.display = "block";
    }

    // Event listeners for arrow buttons
    nextButton.addEventListener("click", function() {
        showNextSlide();
        hideArrows(); // Hide arrows after clicking
    });

    prevButton.addEventListener("click", function() {
        showPrevSlide();
        hideArrows(); // Hide arrows after clicking
    });

    // Auto-play the slideshow
    setInterval(showNextSlide, 3000); // Change slide every 3 seconds

    // Show the first slide initially
    showSlide(currentIndex);

    // Click on the left side of the image to go to previous slide
    slideshowContainer.addEventListener("click", function(event) {
        if (event.offsetX < slideshowContainer.offsetWidth / 2) {
            showPrevSlide();
        } else {
            showNextSlide();
        }
    });
});
