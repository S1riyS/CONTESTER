let currentSidebarY = -1;

function setScrollBarAttributes() {
    let sidebar = $('#sidebar');
    let taskMain = $('#task__main');

    if (currentSidebarY <= 0) currentSidebarY = findPosY(sidebar);

    if (pageYOffset > 70) {
        sidebar.css({
            position: 'fixed',
            top: 20,
            height: 'auto',
        })
        taskMain.addClass("offset-xl-2");
    } else {
        sidebar.css({
            position: 'relative',
            top: 0,
            height: '100%',
        })
        taskMain.removeClass("offset-xl-2");
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

$('a[data-toggle="tab"]').on('shown.bs.tab', function (e) {
    let currentTab = $(this)
    let nextTab = $(this).parent().next('.nav-item').children('.nav-link')

    $('#task_tabs .nav-link').removeClass('hide_after')

    currentTab.addClass('hide_after')
    nextTab.addClass('hide_after')
    console.log(currentTab, nextTab)
})
