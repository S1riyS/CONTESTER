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
