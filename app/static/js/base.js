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
    $('[data-toggle="tooltip"]').tooltip({
        delay: {"show": 400, "hide": 0},
    })
})