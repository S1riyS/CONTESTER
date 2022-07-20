import {showAlert} from "../../../../static/js/modules/alert.js";

$("#create_topic_from").submit(function (event) {
    event.preventDefault();

    let data = {
        grade_id: $('#grade').val(),
        name: $('#topic_name').val()
    }

    $.ajax({
        type: 'POST',
        url: '/api/admin/topic',
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
});