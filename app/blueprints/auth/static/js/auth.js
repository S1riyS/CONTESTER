import {showAlert} from "../../../../static/js/modules/alert.js";

export function sendAuthAjax(url, data) {
    $.ajax({
        type: 'POST',
        url: url,
        contentType: 'application/json;charset=UTF-8',
        data: JSON.stringify(data),
        success: function (response) {
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
}

// Показать/скрыть пароль
$(document).on('click', '.password-control', function () {
    let inputField = $(this).siblings('.form__input').eq(0);

    if (inputField.attr('type') === 'password') {
        $(this).addClass('view');
        inputField.attr('type', 'text');
    } else {
        $(this).removeClass('view');
        inputField.attr('type', 'password');
    }
});
