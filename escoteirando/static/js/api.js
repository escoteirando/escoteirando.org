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

function fetch_post(route, values) {
    fd = new FormData()
    for (let name in values) {
        fd.append(name, values[name])
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

async function login(username, password, remember) {
    fd = new FormData()
    fd.append('username', username);
    fd.append('password', password);
    fd.append('remember', remember);
    let success = false;
    // fetch(api_bu + 'login', {
    //         method: 'POST',
    //         cache: 'no-cache',
    //         body: fd
    //     })
    //     .then(json => {
    //         console.log('Login: ', response);
    //         success = response.ok;
    //     })
    let response = await fetch(api_bu + 'login', {
        method: 'POST',
        cache: 'no-cache',
        body: fd
    });
    console.log('Login:', response)
    success = response.ok;
    return success;
}