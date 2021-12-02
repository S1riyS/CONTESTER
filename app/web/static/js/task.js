let currentSidebarY = -1;

$(function () {
    $(window).scroll(function () {
        let sidebar = $('#sidebar');
        let task = $('#task');

        if (currentSidebarY <= 15) currentSidebarY = findPosY(sidebar);

        if (pageYOffset > currentSidebarY - 15) {
            sidebar.css({
                position: 'fixed',
                top: 15,
                height: 'auto',
            })
            task.addClass("offset-xl-2");
        } else {
            sidebar.css({
                position: 'relative',
                top: 0,
                height: '100%',
            })
            task.removeClass("offset-xl-2");
        }

    });
});

function findPosY(obj) {
    let offset = obj.offset()
    return offset.top - $(window).scrollTop()
}