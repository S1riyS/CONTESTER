import {showAlert} from "./alert.js";

export function sendDefaultAjax(requestType, url, data) {
    $.ajax({
        type: requestType,
        url: url,
        contentType: 'application/json;charset=UTF-8',
        data: JSON.stringify(data),
        success: function (response) {
            let type;

            if (response['success']) {
                type = 'success'
            } else {
                type = 'danger'
            }
            showAlert(response['message'], type);
        },
        error: function (xhr, textStatus, error) {
            showAlert('Что-то пошло не так', 'danger');
        }
    });
}

export function sendAjaxWithRedirect(requestType, url, data) {
    $.ajax({
        type: requestType,
        url: url,
        contentType: 'application/json;charset=UTF-8',
        data: JSON.stringify(data),
        success: function (response) {
            window.location = response['redirect_url']
        },
        error: function (error) {
            showAlert('Что-то пошло не так', 'danger');
        }
    });
}