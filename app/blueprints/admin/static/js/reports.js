import {showAlert} from "../../../../static/js/modules/alert.js";

$('button.mark_as_resolved').click(function () {
    let button = $(this)[0];
    let reportID = button.dataset.reportid;

    // Sending AJAX
    $.ajax({
        type: 'DELETE',
        url: '/api/task/report',
        contentType: 'application/json;charset=UTF-8',
        data: JSON.stringify({
            report_id: reportID
        }),
        success: function (response) {
            let alertType;

            if (response['success']) {
                alertType = 'success';

                button.closest('.table_row__wrapper').remove()
                $('.tooltip').tooltip('hide');
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