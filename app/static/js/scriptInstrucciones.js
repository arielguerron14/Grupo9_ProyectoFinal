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
  









