document.addEventListener('DOMContentLoaded', function () {
    const carousel = document.querySelector('#carousel-anual')
    const items = carousel.querySelectorAll('.carousel-item')
    const btnAnterior = document.querySelector('#ano-anterior')
    const btnProximo = document.querySelector('#ano-proximo')

    function atualizarRotulos() {
        const ativo = carousel.querySelector('.carousel-item.active')
        const index = [...items].indexOf(ativo)

        const anoAtual = parseInt(ativo.dataset.ano)
        const anoAnterior = items[index - 1]?.dataset.ano || ''
        const anoProximo = items[index + 1]?.dataset.ano || ''

        btnAnterior.textContent = anoAnterior
        btnProximo.textContent = anoProximo
    }

    // Atualizar quando o slide mudar
    carousel.addEventListener('slid.bs.carousel', atualizarRotulos)

    // Atualizar ao carregar
    atualizarRotulos()

    function atualizarCalendario() {
        const carousel = document.querySelector('#carousel-anual');
        const ativo = carousel.querySelector('.carousel-item.active');
        const ano = ativo?.dataset.ano;
        if (!ano) return;

        fetch(`/calendario/${ano}`)
            .then(res => res.text())
            .then(html => {
                const container = document.querySelector('#calendario-mensal');
                container.innerHTML = html;
        });
    }


    // escutar o evento de slide
    // const carousel = document.querySelector('#carousel-anual');
    carousel.addEventListener('slid.bs.carousel', atualizarCalendario);

    // chamar uma vez ao carregar a página
    atualizarCalendario();


//     function montarCalendario(data) {
//         const calendarioContainer = document.querySelector('#calendario-mensal');
//         calendarioContainer.innerHTML = '';

//         // para cada mês retornado
//         for (const [mes, dias] of Object.entries(data)) {
//             const divMes = document.createElement('div');
//             divMes.classList.add('mes-container', 'mb-4');

//             // título do mês
//             const titulo = document.createElement('h4');
//             titulo.textContent = `Mês ${mes}`;
//             divMes.appendChild(titulo);

//             // tabela do calendário
//             const tabela = document.createElement('table');
//             tabela.classList.add('table', 'text-center');

//             const thead = document.createElement('thead');
//             thead.innerHTML = `
//             <tr>
//                 <th>Seg</th>
//                 <th>Ter</th>
//                 <th>Qua</th>
//                 <th>Qui</th>
//                 <th>Sex</th>
//                 <th>Dom</th>
//                 <th>Sáb</th>
//             </tr>
//             `;
//             tabela.appendChild(thead);

//             const tbody = document.createElement('tbody');
            
//             // descobrir em qual dia da semana começa o mês
//             // const ano = parseInt(document.querySelector('.carousel-item.active').dataset.ano);
//             const primeiroDia = 0 //new Date(ano, mes - 1, 1).getDay(); // 0 = domingo, 1 = segunda, ...

//             let semana = document.createElement('tr');
//             let diaAtual = 1;

//             // preencher os espaços em branco antes do 1º dia
//             // for (let i = 0; i < primeiroDia; i++) {
//             //     semana.appendChild(document.createElement('td'));
//             // }

//             // preencher os dias
//             dias.forEach((dia, index) => {
//                 const td = document.createElement('td');

//                 if (dia == 0) {
//                     semana.appendChild(td);
//                     primeiroDia = primeiroDia + 1
//                 } else {
//                     td.textContent = dia;
//                     semana.appendChild(td);
//                 }

//                 // se chegou no sábado (6ª célula completa), fecha a semana e começa outra
//                 if ((primeiroDia + index) % 7 === 6) {
//                     tbody.appendChild(semana);
//                     semana = document.createElement('tr');
//                 }
//             });

//             // adiciona a última semana se tiver sobrado
//             if (semana.children.length > 0) {
//                 // completa a linha com espaços vazios se necessário
//                 while (semana.children.length < 7) {
//                     semana.appendChild(document.createElement('td'));
//                 }

//                 tbody.appendChild(semana);
//             }

//             tabela.appendChild(tbody);
//             divMes.appendChild(tabela);
//             calendarioContainer.appendChild(divMes);
//         }
//     }
})
