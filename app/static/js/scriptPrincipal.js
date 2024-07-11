document.addEventListener('DOMContentLoaded', (event) => {
    let timerElement = document.getElementById('timer');
    let time = 1; // time in seconds
    const textoElement = document.getElementById('texto');
    const changeTextButton = document.getElementById('changeTextButton');
    let currentImageIndex = 0; // Índice de la imagen inicial
    
    // Define tus URLs de imágenes aquí
    const images = [
        {id: "img1", src:'../static/img/imgtest1-09.png'},
        {id: "img2", src:'../static/img/imgtest2-09.png'},
        {id: "img3", src:'../static/img/imgtest3-09.png'},
        {id: "img4", src:'../static/img/imgtest4-09.png'},
        {id: "img5", src:'../static/img/imgtest5-09.png'},
        {id: "img6", src:'../static/img/imgtest6-09.png'},
        {id: "img7", src:'../static/img/imgtest7-09.png'},
        {id: "img8", src:'../static/img/imgtest8-09.png'},
        {id: "img9", src:'../static/img/imgtest9-09.png'},
        {id: "img10", src:'../static/img/imgtest10-09.png'}
    ];

    // Establece la imagen inicial
    document.querySelector('.image-container img').src = images[0].src;

    // Agrega tus elementos de texto aquí
    const textElements = [
        document.getElementById('text1'),
        document.getElementById('text2'),
        document.getElementById('text3'),
        document.getElementById('text4'),
        document.getElementById('text5'),
        document.getElementById('text6'),
        document.getElementById('text7'),
        document.getElementById('text8'),
        document.getElementById('text9'),
        document.getElementById('text10')
    ];

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
        const video = document.createElement('video');
        video.setAttribute('autoplay', '');
        video.setAttribute('playsinline', '');
        video.setAttribute('width', '200'); // Ajusta el ancho del video
        video.setAttribute('height', '200'); // Ajusta la altura del video
        profileContainer.appendChild(video);
        navigator.mediaDevices.getUserMedia(constraints)
            .then((stream) => {
                video.srcObject = stream;
            })
            .catch((error) => {
                console.error('Error accessing the webcam', error);
            });
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
    recognition.onend = (event) => {
        console.log('El micro deja de escuchar');
    };
    recognition.onerror = (event) => {
        console.error(event.error);
    };
    document.getElementById('btnStartRecord').addEventListener('click', () => {
        recognition.start();
    });
    document.getElementById('btnStopRecord').addEventListener('click', () => {
        recognition.stop();
    });

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