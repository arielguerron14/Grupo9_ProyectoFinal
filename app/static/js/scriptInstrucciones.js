function animateContainer() {
    const container = document.querySelector('.container');
    container.classList.add('animate__animated', 'animate__fadeIn');
}

if ('speechSynthesis' in window) {
    // El navegador admite la Web Speech API
  } else {
    // El navegador no admite la Web Speech API
    console.log('Tu navegador no admite la Web Speech API');
}
  
// Función para iniciar la síntesis de voz al cargar la página
window.addEventListener('DOMContentLoaded', (event) => {
    // Obtener el elemento de audio oculto
    const audioInstructions = document.getElementById('audioInstructions');
    
    // Texto que se leerá en voz alta
    const instructionsText = "El propósito de este cuestionario es conocer qué tipo de persona ha sido usted. Para contestar el siguiente test, sé honesto contigo mismo: Responde cada pregunta de la manera más sincera posible. Las páginas siguientes contienen una serie de frases usuales o expresiones que las personas suelen utilizar para describirse a sí mismas. Sirven para ayudarle a describir sus sentimientos y actitudes. No se preocupe si algunas cuestiones o frases le parecen extrañas, están incluidas para describir los diferentes problemas que puede tener la gente. Procure responder a todas las frases aunque no esté totalmente seguro. Es mejor contestar a todas para tener un diagnóstico correcto.";
    
    // Crear un objeto de síntesis de voz y configurar el texto a hablar
    const synthesis = new SpeechSynthesisUtterance(instructionsText);

    // Configurar el idioma de la síntesis de voz (opcional)
    synthesis.lang = 'es-ES';

    // Reproducir el texto en voz alta
    window.speechSynthesis.speak(synthesis);

    // Reproducir el texto en el elemento de audio oculto para asegurar la reproducción automática en algunos navegadores
    audioInstructions.src = `data:audio/wav;base64,${window.btoa(instructionsText)}`;
});

// Función para activar la animación cuando se carga la página
window.addEventListener('DOMContentLoaded', (event) => {
    // Obtener los elementos de texto que deseas animar
    const headerElement = document.querySelector('.container h2');
    const paragraphElements = document.querySelectorAll('.container p');
    
    // Agregar una clase para activar la animación al texto
    headerElement.classList.add('animate-text');
    paragraphElements.forEach(paragraph => {
        paragraph.classList.add('animate-text');
    });
});






