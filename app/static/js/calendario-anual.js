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

})