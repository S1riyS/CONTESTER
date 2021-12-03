let currentSidebarY = -1;

function setScrollBarAttributes() {
    let sidebar = $('#sidebar');
    let task = $('#task');

    if (currentSidebarY <= 0) currentSidebarY = findPosY(sidebar);

    if (pageYOffset > 70) {
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
}

function findPosY(obj) {
    let offset = obj.offset()
    return offset.top - $(window).scrollTop()
}

window.onload = function () {
    setScrollBarAttributes()
}
$(window).scroll(function () {
    setScrollBarAttributes()
});