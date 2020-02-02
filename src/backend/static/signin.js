$(document).ready(function () {
    $('#signin').on('submit', (e) => {
        e.preventDefault();

        const user = document.getElementById('inputUser');
        const pass = document.getElementById('inputPass');
        const rem = document.getElementById('inputRem');

        const formdata = new FormData();
        formdata.append('username', user.value);
        formdata.append('password', pass.value);
        formdata.append('rem', rem.value);
        params = {
            method: 'POST',
            headers: { 'Accept': 'application/json' },
            body: formdata
        }

        fetch('/auth/login', params)
            .then((response) => {
                console.log(response);
                if (response.ok) {                    
                    document.location.reload();
                } else {
                    response.json()
                        .then((json) => {
                            alert(json.message)
                        })
                }
            })

    })
});