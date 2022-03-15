import {sendAuthAjax} from "./auth.js";

$('#login_form').submit(function (event) {
    event.preventDefault()

    let data = {
        email: $('#email').val(),
        password: $('#password').val(),
    }

    sendAuthAjax('/api/auth/login', data)
})