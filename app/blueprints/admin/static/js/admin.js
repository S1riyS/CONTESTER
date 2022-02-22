$(document).ready(function () {
    //jquery for toggle sub menus
    $('.sub-btn').click(function () {
        $(this).closest('.item').toggleClass('active')
        $(this).next('.sub-menu').slideToggle();
        $(this).find('.dropdown').toggleClass('rotate');
    });
});


$(".textarea_auto_expand").keyup(function (e) {
    $(this).css({'height': '56px'})
    let borderTopWidth = parseFloat($(this).css("borderTopWidth"));
    let borderBottomWidth = parseFloat($(this).css("borderBottomWidth"))
    while ($(this).outerHeight() < this.scrollHeight + borderTopWidth + borderBottomWidth) {
        $(this).height($(this).height() + 1);
    }
});

$(".dropdown-menu a").click(function () {
    // Remove any existing 'active' classes...
    $(this).closest('.dropdown-menu').find('a').removeClass('active');

    // Add 'active' class to clicked element...
    $(this).addClass('active');

    let dropdownMenuButton = $(this).closest('.dropdown-menu').siblings('.dropdown-btn')
    let dropdownMenuText =  dropdownMenuButton.find('.dropdownBtn__text')
    dropdownMenuText.html($(this).text())
});