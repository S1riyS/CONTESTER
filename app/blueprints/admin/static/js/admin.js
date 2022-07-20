function setDropdownItem(item) {
    let dropdownMenuButton = item.closest('.dropdown-menu').siblings('.dropdown-btn');
    let dropdownMenuText = dropdownMenuButton.find('.dropdownBtn__text');
    let text = item.text()
    dropdownMenuText.html(text)
}

$(document).ready(function () {
    //jquery for toggle sub menus
    $('.sub-btn').click(function () {
        $(this).closest('.item').toggleClass('active')
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

$('.dropdown-item.active').each(function () {
    setDropdownItem($(this))
})

$(".dropdown-menu").on('click', '.dropdown-item:not(.dropdown-link-item)', function () {
    // Remove any existing 'active' classes...
    $(this).closest('.dropdown-menu').find('a').removeClass('active');

    // Add 'active' class to clicked element...
    $(this).addClass('active');

    setDropdownItem($(this))
});

$('#dropdown__grade .dropdown-item').click(function () {
    let topicDropdownList = $('#dropdownMenuTopic')

    let data = {
        grade_id: $(this).data('value')
    }

    $.ajax({
        type: 'POST',
        url: '/api/topics',
        contentType: 'application/json;charset=UTF-8',
        data: JSON.stringify(data),
        success: function (response) {
            topicDropdownList.html(response);
            let activeTopic = topicDropdownList.find('.dropdown-item.active')
            let dropdownButton = topicDropdownList.siblings('.dropdown-btn')

            if (activeTopic.length) {
                setDropdownItem(activeTopic)
                dropdownButton.removeClass('empty-dropdown')
            } else {
                $('#dropdown_topic__text').html('Темы не найдены')
                dropdownButton.addClass('empty-dropdown')
            }
        },
        error: function (error) {
            console.log(error);
        }
    })
})