$(document).ready(function () {
    //jquery for toggle sub menus
    $('.sub-btn').click(function () {
        $(this).toggleClass('active')
        $(this).closest('.item').toggleClass('active');
        $(this).next('.sub-menu').slideToggle();
        $(this).find('.dropdown').toggleClass('rotate');
    });
});


$(".auto_expand").keyup(function (e) {
    $(this).css({'height': '56px'})
    let borderTopWidth = parseFloat($(this).css("borderTopWidth"));
    let borderBottomWidth = parseFloat($(this).css("borderBottomWidth"))
    while ($(this).outerHeight() < this.scrollHeight + borderTopWidth + borderBottomWidth) {
        $(this).height($(this).height() + 1);
    }
});
