function abrirPopupExplicativo(elemento) {
    const titulo = elemento.getAttribute('data-titulo');
    const data = elemento.getAttribute('data-data');
    const inicio = elemento.getAttribute('data-horario-inicio');
    const fim = elemento.getAttribute('data-horario-fim');
    const descricao = elemento.getAttribute('data-descricao');
    const local = elemento.getAttribute('data-local');
    const categoria = elemento.getAttribute('data-categoria');
    const dia_semana = elemento.getAttribute('data-dia-semana');

    document.querySelector('.popup-content h2').textContent = titulo;
    document.querySelector('.popup-content .data').textContent = data;
    document.querySelector('.dia-semana p').textContent = dia_semana;
    document.querySelector('.horarios .inicio').textContent = `${inicio.slice(0, 5)}`;
    document.querySelector('.horarios .fim').textContent = `${fim.slice(0, 5)}`;
    document.querySelector('.local').textContent = local;
    document.querySelector('.categoria').textContent = categoria;
    document.querySelector('.descricao').textContent = descricao;

    document.getElementById('popup-explicativo').style.display = 'flex';
}

// Função para fechar o popup
function closePopup() {
  document.getElementById('popup-explicativo').style.display = 'none';
}