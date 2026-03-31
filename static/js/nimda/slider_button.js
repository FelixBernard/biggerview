document.addEventListener('DOMContentLoaded', function() {
    const slider = document.querySelector('.slider');
    const buttons = document.querySelectorAll('.slider-btn');
    const sliderContainer = document.querySelector('.glossy-slider');
    let currentChart = 'line';

    // Button-Logik
    buttons.forEach(button => {
        button.addEventListener('click', function() {
            // Berechne die Breite eines Buttons
            const buttonWidth = sliderContainer.clientWidth / buttons.length;

            // Setze die Position des Sliders
            if (this.dataset.chart === 'line') {
                slider.style.left = '5px';
                slider.style.width = `calc(${buttonWidth}px - 10px)`;
            } else {
                slider.style.left = `calc(${buttonWidth}px + 5px)`;
                slider.style.width = `calc(${buttonWidth}px - 10px)`;
            }

            // Aktiven Button markieren
            buttons.forEach(btn => btn.classList.remove('active'));
            this.classList.add('active');
        });
    });

    // Initialisierung: Setze die Breite des Sliders beim Laden der Seite
    window.addEventListener('resize', function() {
        const buttonWidth = sliderContainer.clientWidth / buttons.length;
        if (currentChart === 'line') {
            slider.style.left = '5px';
        } else {
            slider.style.left = `calc(${buttonWidth}px + 5px)`;
        }
        slider.style.width = `calc(${buttonWidth}px - 10px)`;
    });

    // Initialisierung beim Laden der Seite
    const buttonWidth = sliderContainer.clientWidth / buttons.length;
    slider.style.width = `calc(${buttonWidth}px - 10px)`;
});