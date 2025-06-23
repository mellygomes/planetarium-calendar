const meses = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"];

// Função para abrir o popup
function openPopup(elemento) {
  if (document.getElementById('popup-explicativo').style.display != 'flex') {
    const data = elemento.getAttribute('data-data');
    document.getElementById('data_evento').value = data;


    // opcional: mostrar a data na interface também
    const [ano, mes, dia] = data.split('-');
    const dataVisual = 'testeeeee'// `${dia} de ${meses[parseInt(mes, 10)]} de ${ano}`; // O parseInt serve pra tirar o zero à esquerda

    document.querySelector('.popup-content p').textContent = dataVisual;
    console.log(dataVisual)

  
      document.getElementById('popup').style.display = 'flex';
  }
}

// Função para fechar o popup
function closePopup() {
  document.getElementById('popup').style.display = 'none';
}

function abrirPopupExplicativo(elemento) {
    const data = elemento.getAttribute('data-data');
    const [ano, mes, dia] = data.split('-');
    const dataVisual = `${dia} de ${meses[parseInt(mes - 1, 10)]}`; // O parseInt serve pra tirar o zero à esquerda

    const titulo = elemento.getAttribute('data-titulo');
    const inicio = elemento.getAttribute('data-horario-inicio');
    const fim = elemento.getAttribute('data-horario-fim');
    const descricao = elemento.getAttribute('data-descricao');
    const local = elemento.getAttribute('data-local');
    const categoria = elemento.getAttribute('data-categoria');
    const dia_semana = elemento.getAttribute('data-dia-semana');

    document.querySelector('.popup-content h2').textContent = titulo;
    document.querySelector('.popup-content .data').textContent = dataVisual;
    document.querySelector('.dia-semana p').textContent = dia_semana;
    document.querySelector('.horarios .inicio').textContent = `${inicio.slice(0, 5)}`;
    document.querySelector('.horarios .fim').textContent = `${fim.slice(0, 5)}`;
    document.querySelector('.local').textContent = local;
    document.querySelector('.categoria').textContent = categoria;
    document.querySelector('.descricao').textContent = descricao;

    document.getElementById('popup-explicativo').style.display = 'flex';
}

// Função para fechar o popup
function closePopupExplicativo() {
  document.getElementById('popup-explicativo').style.display = 'none';
}
