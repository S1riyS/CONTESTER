import {showAlert} from "./modules/alert.js";


$(function () {
    $('[data-tooltip="tooltip"]').tooltip({
        delay: {"show": 400, "hide": 0},
        trigger: 'hover'
    })
})

$(function () {
    $('ul.tabs_caption').on('click', 'li:not(.active)', function () {
        $(this).addClass('active').siblings().removeClass('active').closest('div.tabs').children('div.tabs_content').removeClass('active').eq($(this).index()).addClass('active');
    });
});

$('#logout').click(function () {
    $.ajax({
        type: 'POST',
        url: '/api/auth/logout',
        contentType: 'application/json;charset=UTF-8',
        success: function (response) {
            localStorage.setItem('taskStorage', JSON.stringify({}));
            window.location = response['redirect_url'];
        },
        error: function (error) {
            showAlert('Что-то пошло не так', 'danger');
        }
    });
})

$('#confirmEmailButton').on('click', function () {
    $('#confirmEmailModal').modal('hide');

    $.ajax({
        type: 'PUT',
        url: '/api/auth/confirm-email',
        contentType: 'application/json;charset=UTF-8',
        success: function (response) {
            let alertType;

            if (response['success']) {
                alertType = 'success'
            } else {
                alertType = 'danger'
            }

            showAlert(response['message'], alertType);
        },
        error: function (xhr, textStatus, error) {
            showAlert('Что-то пошло не так', 'danger');
        }
    });
})