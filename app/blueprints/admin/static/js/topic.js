import {sendDefaultAjax} from "../../../../static/js/modules/send_ajax.js";

function collectTopicData() {
    return {
        grade_id: $('#grade_id').val(),
        name: $('#name').val()
    }
}

$("#create_topic_from").submit(function (event) {
    event.preventDefault();
    sendDefaultAjax('POST', '/api/admin/topic', collectTopicData())
});

$("#edit_topic_from").submit(function (event) {
    event.preventDefault();
    let URLParams = new window.URLSearchParams(window.location.search);
    if (URLParams.has('id')) {
        let id = URLParams.get('id')
        sendDefaultAjax('PUT', `/api/admin/topic/${id}`, collectTopicData())
    }
});