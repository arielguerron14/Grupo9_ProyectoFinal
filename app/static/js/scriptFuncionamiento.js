document.addEventListener("DOMContentLoaded", function() {
    const texts = document.querySelectorAll('.text');
    let currentIndex = 0;

    function showText(index) {
        texts.forEach((text) => {
            text.classList.remove('active');
        });
        texts[index].classList.add('active');
        speakText(texts[index].innerText);
    }

    function toggleText() {
        // Incrementa currentIndex solo si no se ha alcanzado el último texto
        if (currentIndex < texts.length - 1) {
            currentIndex++;
            showText(currentIndex);
        } else {
            // Si ya se mostró el último texto, no hace nada para detener el ciclo
            console.log("Último texto leído");
        }
    }

    function speakText(text) {
        const speech = new SpeechSynthesisUtterance(text);
        speech.lang = 'es-ES'; // Establece el idioma del texto a español
        speech.onend = function(event) {
            toggleText(); // Cambia al siguiente texto una vez que termine de leer el actual
        };
        window.speechSynthesis.speak(speech);
    }

    // Inicialmente mostrar el primer texto
    showText(currentIndex);
});
