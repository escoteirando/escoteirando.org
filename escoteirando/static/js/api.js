class API {
    constructor() {}

    async login(username, password, remember) {
        return await api.post('login', { 'username': username, 'password': password, 'remember': remember });
    }

    async logout() {
        if (await api.get('logout')) {
            location.replace('/');
        }
    }

    async signup(username, password) {
        return await api.post('signup', {
            "username": username,
            "password": password
        });
    }
}


class APIFetch {
    constructor() {
        this.api_bu = '/api/v1/';
        this.last_message = '';
        this.last_success = false;
        this.last_data = null;
        this.last_request = null;
        this.last_timing = 0;
    }

    async api_fetch(route, options) {
        let t0 = performance.now();
        let success = false;
        try {
            let response = await fetch(this.api_bu + route, options);
            let json = null;
            if (response.ok) {
                json = await response.json();
            }
            this.last_success = response.ok;
            this.last_data = json;
            this.last_message = response.statusText
            this.last_request = options.method + ' ' + route;
            this.last_timing = performance.now() - t0;
            Base.debug(this);
            success = response.ok;

        } catch (error) {
            console.error(error);
        }
        return success;




    }

    async get(route, values = null) {
        let options = {
            method: 'GET',
            cache: 'no-cache'
        }
        if (values) {
            options['body'] = values;
        }
        return await this.api_fetch(route, options)
    }

    async post(route, values = null) {
        var options = {
            method: 'POST',
            cache: 'no-cache'
        }
        if (values) {
            let fd = new FormData()
            for (let name in values) {
                fd.append(name, values[name])
            }
            options['body'] = fd
        }
        return await this.api_fetch(route, options)
    }

    post_async(route, values = null, on_success, on_fail) {
        var options = {
            method: 'POST',
            cache: 'no-cache'
        }
        if (values) {
            let fd = new FormData()
            for (let name in values) {
                fd.append(name, values[name])
            }
            options['body'] = fd
        }
        fetch(this.api_bu + route, options)
            .then(response => response.json())
            .then(json => {
                on_success(json);
            })
            .catch()
    }
}

const api = new APIFetch()