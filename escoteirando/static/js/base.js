$(() => {
    let back_to_top = document.getElementById('back_to_top');
    window.addEventListener('scroll', () => {
        back_to_top.style = window.scrollY == 0 ? "display:none" : "";
    })
})