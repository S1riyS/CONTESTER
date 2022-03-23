import {showAlert} from "./modules/alert.js";

let cords = ['scrollX', 'scrollY'];
// сохраняем позицию скролла в localStorage
window.addEventListener('beforeunload', e => cords.forEach(cord => localStorage[cord] = window[cord]));
// вешаем событие на загрузку (ресурсов) страницы
window.addEventListener('load', e => {
    // если в localStorage имеются данные
    if (localStorage[cords[0]]) {
        // скроллим к сохраненным координатам
        window.scroll(...cords.map(cord => localStorage[cord]));
        // удаляем данные с localStorage
        cords.forEach(cord => localStorage.removeItem(cord));
    }
});

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
                let type;

                if (response['success']) {
                    type = 'success'
                } else {
                    type = 'danger'
                }
                showAlert(response['message'], type);
            },
            error: function (error) {
                showAlert('Что то пошло не так', 'danger');
            }
    });
})