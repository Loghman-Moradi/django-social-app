// const btns = document.querySelectorAll('ul li');
// const previous = document.getElementById('previous');
// const next = document.getElementById('next');
//
// let currentIndex = 0;
//
// updateButtonState();
//
// for (let i = 0; i < btns.length; i++) {
//   btns[i].addEventListener('click', function() {
//     currentIndex = i;
//     updateActiveClass();
//     updateButtonState();
//   });
// }
//
// previous.addEventListener('click', function() {
//   currentIndex = (currentIndex - 1 + btns.length) % btns.length;
//   updateActiveClass();
//   updateButtonState();
// });
//
// next.addEventListener('click', function() {
//   currentIndex = (currentIndex + 1) % btns.length;
//   updateActiveClass();
//   updateButtonState();
// });
//
// function updateActiveClass() {
//   let current = document.querySelector('.active');
//   if (current) {
//     current.classList.remove('active');
//   }
//   btns[currentIndex].classList.add('active');
// }
//
// function updateButtonState() {
//   previous.disabled = currentIndex === 0;
//   next.disabled = currentIndex === btns.length - 1;
// }
//
//
// const buttons = document.querySelectorAll('button');
// buttons.forEach(btn => {
//   btn.addEventListener('click', () => {
//     btn.classList.add('active');
//     setTimeout(() => {
//       btn.classList.remove('active');
//     }, 600)
//   })
// })