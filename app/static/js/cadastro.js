document.getElementById("form-cadastro").addEventListener('submit', function(event) {
    event.preventDefault() // evitar o recarregamento da tela

    const nome = document.getElementById('nome').value;
    const email = document.getElementById('email').value;
    const senha = document.getElementById('senha').value;
})