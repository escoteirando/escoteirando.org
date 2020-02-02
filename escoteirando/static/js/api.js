let api_bu = '/api/v1/';

async function logout() {
    let response = await fetch(api_bu + 'logout', {
        method: 'GET',
        cache: 'no-cache'
    })
    if (response.ok) {
        location.replace("/");
    }
}

function fetch_post(route, values = null) {
    options = {
        method: 'POST',
        cache: 'no-cache'
    }
    if (values) {
        fd = new FormData()
        for (let name in values) {
            fd.append(name, values[name])
        }
        options['body'] = fd
    }
    // https://javascript.info/fetch
    // TODO: Continuar a desenvolver o fetch_post
    let response = await fetch(api_bu + route, options)
    if (!response.ok) {
        return
    }
    let success = false;
    let result = null;
    fetch(api_bu + route, {
            method: 'POST',
            cache: 'no-cache',
            body: fd
        })
        .then(response => {
            success = response.ok;
            return response.json()
        })
        .then(data => {
            success = true;
            result = data;
        })
    return result;
}

function login(username, password, remember) {
    fd = new FormData()
    fd.append('username', username);
    fd.append('password', password);
    fd.append('remember', remember);
    let success = false;
    let response = await fetch(api_bu + 'login', {
        method: 'POST',
        cache: 'no-cache',
        body: fd
    });
    console.log('Login:', response)
    success = response.ok;
    return success;
}

function signup(username, password) {
    fd = new FormData()
    fd.append('username', username);
    fd.append('password', password);
    let success = false;
    let response = await fetch(api_bu + 'signup', {
        method: 'POST',
        cache: 'no-cache',
        body: fd
    });
    console.log('Signup:', response)
    success = response.ok;
    return success;
}