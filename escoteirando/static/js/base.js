$(() => {
    let back_to_top = document.getElementById('back_to_top');
    if (back_to_top) {
        window.addEventListener('scroll', () => {
            back_to_top.style = window.scrollY == 0 ? "display:none" : "";
        })
    }
})

function getFieldValues(...ids) {
    let values = {}
    for (i = 0; i < ids.length; i++) {
        elm = document.getElementById(ids[i]);
        value = elm == null ? null : (elm.type == 'checkbox' ? elm.checked : elm.value);
        name = ids[i];
        values[name] = value
    }
    return values;
}

function createElement(name, classes = null, id = null, attributes = null) {
    elm = document.createElement(name);
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

function createAlert(alert_content, class_name = "default", timeout = 0) {
    let alert_placeholder = document.getElementById('alert_placeholder');
    if (alert_placeholder == null) {
        log.error("createAlert: #alert_placeholder does not exists!");
        log.warn("Alert: [" + alert_class + "] = " + alert_content + "]");
        return;
    }
    // alert_placeholder.innerText = ''
    // let div_alert = createElement('div', 'alert alert-' + class_name + ' alert-dismissible show', 'div_alert', { role: "alert" });
    // let div_button = createElement('button', 'close', null, { "type": "button", "data-dismiss": "alert", "aria-label": "Close" });
    // let span = createElement('span', null, null, { "aria-hidden": true })
    // span.innerText = '&times;'
    // div_button.appendChild(span);
    // div_alert.innerText = text;
    // div_alert.appendChild(div_button);

    alert_placeholder.innerHTML = '<div class="alert alert-' + class_name + ' alert-dismissible show" id="div_alert" role="alert">' +
        alert_content + '<button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span>' +
        '</button></div>';
    $('#div_alert').alert()
    if (timeout > 0) {
        setTimeout(() => $('#div_alert').remove(), timeout * 1000);
    }
}