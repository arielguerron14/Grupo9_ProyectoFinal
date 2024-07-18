document.addEventListener('DOMContentLoaded', (event) => {
    let timerElement = document.getElementById('timer');
    let time = 1; // time in seconds
    const textoElement = document.getElementById('texto');
    const changeTextButton = document.getElementById('changeTextButton');
    let currentImageIndex = 0; // Índice de la imagen inicial     

    // Establece la imagen inicial
    document.querySelector('.image-container img').src = images[0].src;

    // Agrega tus elementos de texto aquí
    

    // Oculta todos los textos al inicio
    textElements.forEach(textElement => textElement.style.display = 'none');

    // Muestra el primer texto
    textElements[0].style.display = 'block';

    // Reproduce la voz del primer texto
    speakText(textElements[0].textContent);

    function updateTimer() {
        let minutes = Math.floor(time / 60).toString().padStart(2, '0');
        let seconds = (time % 60).toString().padStart(2, '0');
        timerElement.textContent = `${minutes}:${seconds}`;
        time++;
    }
    setInterval(updateTimer, 1000);

    function startWebcam() {
        // Implementación de la función para iniciar la cámara web
        const constraints = {
            video: {
                width: { exact: 200 }, // Establece el ancho exacto de la cámara
                height: { exact: 200 } // Establece la altura exacta de la cámara
            }
        };
        const profileContainer = document.querySelector('.profile-container');
        if (!profileContainer) {
            console.error('Profile container not found.');
            return;
        }
        const existingImage = profileContainer.querySelector('img');
        if (existingImage) {
            existingImage.remove();
        }
        
    }

    function detectEmotion(imageUrl) {
        // Implementación de la función para detectar emociones
    }

    let recognition = new webkitSpeechRecognition();
    recognition.lang = 'es-MX';
    recognition.continuous = true;
    recognition.interimResults = false;
    recognition.onresult = (event) => {
        const results = event.results;
        const frase = results[results.length - 1][0].transcript;
        textoElement.value += frase + ' '; // Añade un espacio después de cada frase
    };
    
    recognition.onerror = (event) => {
        console.error(event.error);
    };
   
    function speakText(text) {
        const speech = new SpeechSynthesisUtterance(text);
            speech.lang = 'es-ES'; // Establece el idioma del texto a español
        window.speechSynthesis.speak(speech);
    }
    function changeImageAndText() {
        // Oculta el texto actual
        textElements[currentImageIndex].style.display = 'none';

        // Avanza al siguiente índice
        currentImageIndex = (currentImageIndex + 1) % images.length;

        // Muestra el nuevo texto
        textElements[currentImageIndex].style.display = 'block';

        // Reproduce la voz del texto
        speakText(textElements[currentImageIndex].textContent);

        // Cambia la imagen
        document.querySelector('.image-container img').src = images[currentImageIndex].src;

        // Limpia el textarea
        textoElement.value = '';
    }
    function sendData() {
        const data = {
            texto: textoElement.value,
            imagen_actual: images[currentImageIndex].id
        };
        fetch('/guardar_respuesta', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
        .then(response => {
            if (response.ok) {
                changeImageAndText();
            } else {
                console.error('Error al enviar datos');
            }
        })
        .catch((error) => {
            console.error('Error:', error);
        });
    }
    changeTextButton.addEventListener('click', sendData);
    // Inicializar webcam al cargar la página
    startWebcam();
});