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
})
