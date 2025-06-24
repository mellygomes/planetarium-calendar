dias_semana = ['Segunda-feira', 'Terça-feira', 'Quarta-feira', 'Quinta-feira', 'Sexta-feira', 'Sábado', 'Domingo']

document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll(".item-lista-eventos").forEach(el => {
    formatarDataHora(el);
  });
});

function formatarDataHora(elemento) {
    const data = elemento.getAttribute('data-data');
    const [ano, mes, dia] = data.split('-');
    const data_visual = `${dia} de ${meses[parseInt(mes, 10) - 1]}`;

    const dataObj = new Date(data);
    const dia_semana = dias_semana[dataObj.getDay()];
    const inicio = elemento.getAttribute('data-inicio');
    const fim = elemento.getAttribute('data-fim');

    elemento.querySelector('.inicio-item').textContent = `${inicio.slice(0, 5)}`;
    elemento.querySelector('.fim-item').textContent = `${fim.slice(0, 5)}`;
    elemento.querySelector('.dia-semana-item').textContent = dia_semana;
    elemento.querySelector('.data-dia-item').textContent = data_visual;
}


const meses = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"];

function abrirPopupExplicativo(elemento) {
    const data = elemento.getAttribute('data-data');
    const titulo = elemento.getAttribute('data-titulo');
    const inicio = elemento.getAttribute('data-horario-inicio');
    const fim = elemento.getAttribute('data-horario-fim');
    const descricao = elemento.getAttribute('data-descricao');
    const local = elemento.getAttribute('data-local');
    const categoria = elemento.getAttribute('data-categoria');

    const [ano, mes, dia] = data.split('-');
    const data_visual = `${dia} de ${meses[parseInt(mes, 10) - 1]}`;

    const dataObj = new Date(data);
    const dia_semana = dias_semana[dataObj.getDay()];

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