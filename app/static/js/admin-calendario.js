// document.addEventListener('DOMContentLoaded', function () {
    // Função para abrir o popup
    function openPopup(elemento) {
        const data = elemento.getAttribute('data-data');
        document.getElementById('data_evento').value = data;

        // opcional: mostrar a data na interface também
        const dataVisual = new Date(data).toLocaleDateString('pt-BR');
        document.querySelector('.popup-content p').textContent = `Data selecionada: ${dataVisual}`;


        document.getElementById('popup').style.display = 'flex';
    }

    // Função para fechar o popup
    function closePopup() {
      document.getElementById('popup').style.display = 'none';
    }
// })