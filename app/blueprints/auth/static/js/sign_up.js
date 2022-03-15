import {sendAuthAjax} from "./auth.js";

$('#signup_form').submit(function (event) {
    event.preventDefault()

    let data = {
        firstname: $('#first_name').val(),
        lastname: $('#last_name').val(),
        grade: $('#grade').val(),
        letter: $('#letter').val(),
        email: $('#email').val(),
        password: $('#password').val(),
        password_again: $('#password_again').val()
    }

    sendAuthAjax('/api/auth/sign-up', data)
})