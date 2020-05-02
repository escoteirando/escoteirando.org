class Base {
    static _debugging() {
        return true;
    }

    static debug(msg) {
        if (this._debugging()) {
            console.debug(msg);
        }
    }

    static getFormData(keys) {
        let fd = new FormData()
        for (let [key, name] of Object.entries(keys)) {
            const elm = document.getElementById(key);
            const value = elm == null ? null : (elm.type == 'checkbox' ? elm.checked : elm.value);
            fd.append(name, value);
        }
        return fd;
    }
    static getFieldValues(...ids) {
        let values = {}
        for (let i = 0; i < ids.length; i++) {
            const elm = document.getElementById(ids[i]);
            const value = elm == null ? null : (elm.type == 'checkbox' ? elm.checked : elm.value);
            values[ids[i]] = value
        }
        return values;
    }

    static createElement(name, classes = null, id = null, attributes = null) {
        const elm = document.createElement(name);
        if (classes) {
            elm.className = classes;
        }
        if (id) {
            elm.id = id;
        }
        if (attributes) {
            for (let key in attributes) {
                elm.setAttribute(key, attributes[key]);
            }
        }
        return elm;
    }

    static createAlert(alert_content, class_name = "default", timeout = 0, on_close = null) {
        let alert_placeholder = document.getElementById('alert_placeholder');
        if (alert_placeholder == null) {
            log.error("createAlert: #alert_placeholder does not exists!");
            log.warn("Alert: [" + alert_class + "] = " + alert_content + "]");
            return;
        }

        alert_placeholder.innerHTML = '<div class="alert alert-' + class_name + ' alert-dismissible show" id="div_alert" role="alert">' +
            alert_content + '<button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span>' +
            '</button></div>';
        if (on_close) {
            $('#div_alert').on('closed.bs.alert', on_close);
        }
        $('#div_alert').alert()

        if (timeout > 0) {
            setTimeout(() => {
                $('#div_alert').remove();
                if (on_close) {
                    on_close();
                }
            }, timeout * 1000);
        }
    }

    static _init_back_to_top() {
        let back_to_top = document.getElementById('back_to_top');
        if (back_to_top) {
            window.addEventListener('scroll', () => {
                back_to_top.style = window.scrollY == 0 ? "display:none" : "";
            })
        }
    }

    static init_base() {
        this._init_back_to_top();
    }

    static async logout() {
        const api = new API();
        await api.logout();
    }

}
$(() => {
    Base.init_base()
})