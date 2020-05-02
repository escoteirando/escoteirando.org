$(() => Signin.init());

class Signin {
    constructor() {
        Base.debug('SignIn INIT');
    }

    static async login_mappa(e) {
        Base.debug('SignIn LOGIN MAPPA');
        if (e != null) {
            e.preventDefault();
        }
        let data = Base.getFormData({
            "signinEmail": 'username',
            "signinPassword": 'password'
        });

        var options = {
            method: 'POST',
            cache: 'no-cache',
            body: data,
            contentType: 'multipart/form-data'
        }

        let response = await fetch('/api/v1/mappa/login', options)
        if (response.ok) {
            Base.debug('Login OK');
            Base.createAlert('Login OK', 'success');
            location.assign('/');
        } else {
            let message = await response.json();
            Base.createAlert('Login ERROR: ' + message.msg, 'danger', 10);
            this.debug('Login ERROR:' + message.msg);
        }
    }

    static async login(e) {
        Base.debug('SignIn LOGIN');
        if (e != null) {
            e.preventDefault();
        }

        let data = Base.getFormData({
            "signinEmail": 'username',
            "signinPassword": 'password',
            "signinRemember": "remember"
        });

        var options = {
            method: 'POST',
            cache: 'no-cache',
            body: data,
            contentType: 'multipart/form-data'
        }

        let response = await fetch('/api/v1/login', options)
        if (response.ok) {
            Base.debug('mAPPa Login OK');
            Base.createAlert('mAPPa Login OK', 'success');
            location.assign('/');
        } else {
            let message = await response.json();
            Base.createAlert('mAPPa Login ERROR: ' + message.msg, 'danger', 10);
            this.debug('mAPPa Login ERROR:' + message.msg);
        }
    }

    static async signup(e) {
        Base.debug('SignIn SIGNUP');
        e.preventDefault();
        const api = new API()
        const values = Base.getFieldValues('registerEmail', 'registerPassword');
        const success = api.signup(values.registerEmail, values.registerPassword);
        if (success) {
            Base.createAlert('Usuário registrado com sucesso', 'success', 5000, () => location.reload(true));
        }
    }

    static async recover(e) {
        Base.debug('SignIn RECOVER');
        e.preventDefault();
        [perdiEmail] = Base.getFieldValues('perdiEmail')
        alert('RECUPERAR ' + perdiEmail)
    }

    static init_login() {
        Signin.loginClick('login');
        $(".btn_registrar").on('click', () => Signin.loginClick('register'))
        $(".btn_esqueci").on('click', () => Signin.loginClick('perdi'))
        $(".btn_login").on('click', () => Signin.loginClick('login'))

        let sp = document.getElementById("show-pass");
        sp.onchange = ev => {
            document.getElementById('registerPassword').type = ev.srcElement.checked ? "password" : "text";
        }
        $('#login-tabs li:first-child a').tab('show')
        $('.alert').alert()

        $('#btn_login').on('click', Signin.login);

        $('#btn_registrar').on('click', Signin.signup);

        $('#btn_recuperar').on('click', Signin.recover);
    }

    static init_mappa() {
        $("#btn_login_mappa").on('click', Signin.login_mappa);
    }

    static init() {

        if (login_mappa) {
            Signin.init_mappa();
        } else {
            Signin.init_login();
        }

        Base.debug('escoteirando.org:signin.js ready')
    }

    static loginClick(acao) {
        $("div.card").hide();
        $('#card-' + acao).show();
        Base.debug('loginClick', acao)
    }
}