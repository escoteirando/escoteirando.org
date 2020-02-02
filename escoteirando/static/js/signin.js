$(function() {
    console.log('escoteirando.org:signin.js init')
    loginClick('login');

    $(".btn_registrar").on('click', () => loginClick('register'))
    $(".btn_esqueci").on('click', () => loginClick('perdi'))
    $(".btn_login").on('click', () => loginClick('login'))

    let sp = document.getElementById("show-pass");
    sp.onchange = ev => {
        document.getElementById('registerPassword').type = ev.srcElement.checked ? "password" : "text";
    }
    $('#login-tabs li:first-child a').tab('show')
    $('.alert').alert()

    function getValue(...ids) {
        results = [];
        for (i = 0; i < ids.length; i++) {
            elm = document.getElementById(ids[i]);
            value = elm == null ? null : (elm.type == 'checkbox' ? elm.checked : elm.value);
            results[results.length] = value;
        }
        return results
    }


    $('#btn_login').on('click', async e => {
        e.preventDefault();
        values = getFieldValues('signinEmail', 'signinPassword', 'signinRemember');

        if (await login(values.signinEmail, values.signinPassword, values.signinRemember)) {
            createAlert('Login OK', 'success');
            location.reload(true);
        } else {
            message = await response.json();
            createAlert('Login ERROR: ' + message.msg, 'danger', 10);
        }

    })
    $('#btn_registrar').on('click', e => {
        e.preventDefault();
        [registerEmail, registerPassword] = getValue('registerEmail', 'registerPassword')
        alert('REGISTRAR ' + registerEmail + ' ' + registerPassword)
    })
    $('#btn_recuperar').on('click', e => {
        e.preventDefault();
        [perdiEmail] = getValue('perdiEmail')
        alert('RECUPERAR ' + perdiEmail)
    })
    console.log('escoteirando.org:signin.js ready')
})

function loginClick(acao) {
    $("div.card").hide();
    $('#card-' + acao).show();
    console.log('loginClick', acao)
}