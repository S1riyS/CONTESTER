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

$(document).ready(function () {
    $('.form__input').each(function () {
        $(this).attr({
            'readonly': ""
        });
    });

    $('.form__input').on({
        focus: function () {
            $('.form__input').each(function () {
                $(this).removeAttr('readonly')
            });
        }
    })
});