import {showAlert} from "../../../../static/js/modules/alert.js";

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
    console.log(data)

    $.ajax({
        type: 'POST',
        url: '/api/auth/sign-up',
        contentType: 'application/json;charset=UTF-8',
        data: JSON.stringify(data),
        success: function (response) {
            let type;

            if (response['success']) {
                window.location = response['redirect_url']
            } else {
                showAlert(response['message'], 'danger');
            }
        },
        error: function (xhr, textStatus, error) {
            showAlert('Что-то пошло не так', 'danger');
        }
    });
})