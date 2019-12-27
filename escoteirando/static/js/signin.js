$(function () {
    $('#TabContent a').on('click', function (e) {
        e.preventDefault()
        $(this).tab('show')
    })
    let sp = document.getElementById("show-pass");
    sp.onchange = ev => {
        document.getElementById('registerPassword').type = ev.srcElement.checked ? "password" : "text";
    }
    $('#login-tabs li:first-child a').tab('show')
})
