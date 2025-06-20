// document.getElementsByTagName('p')

document.addEventListener('DOMContentLoaded', function () {
  new Swiper('.carousel-events', {
    slidesPerView: 5,
    spaceBetween: 28,
    navigation: {
      nextEl: '.swiper-button-next',
      prevEl: '.swiper-button-prev',
    },
    breakpoints: {
      320: {
        slidesPerView: 1,
      },
      768: {
        slidesPerView: 2,
      },
      1024: {
        slidesPerView: 5,
      }
    }
  });
});