import {getCurrentTask} from "./modules/current_task.js";

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

function hideSeparators(tabs) {
    $('#task_tabs .nav-link').removeClass('hide_after')

    $(tabs).each(function () {
        $(this).addClass('hide_after')
    })
}

// Hiding tabs separators, setting attributes to scrollbar (on load)
window.onload = function () {
    let activeTab = $('#task_tabs .nav-link.active').first()
    let nextAfterActiveTab = activeTab.parent().next('.nav-item').children('.nav-link')
    hideSeparators([activeTab, nextAfterActiveTab])
    setScrollBarAttributes()
    $(".loader_wrapper").fadeOut("slow");
}

// Setting attributes to scrollbar (on scroll)
$(window).scroll(function () {
    setScrollBarAttributes()
});

// Hiding tabs separators
$('a[data-toggle="tab"]').on('shown.bs.tab', function (e) {
    let currentTab = $(this)
    let nextTab = $(this).parent().next('.nav-item').children('.nav-link')
    hideSeparators([currentTab, nextTab])
})

// Get submissions tabe
$('#submissions-tab').on('shown.bs.tab', function (e) {
    let submissions = $('#submissions__body')
    let submissionsLoader = $('#submissions__loader')

    $.ajax({
        url: '/api/get_submissions',
        type: 'POST',
        contentType: 'application/json;charset=UTF-8',
        // Before send
        beforeSend(jqXHR, settings) {
            submissions.html('')
            submissionsLoader.css({'display': 'flex'});
        },
        // Complete
        complete: function () {
            submissionsLoader.css({'display': 'none'});
        },
        // Success
        success: function (response) {
            submissions.html(response) // Setting generated HTML
        },
        // Error
        error: function () {
            console.log('Error')
        }
    })
})

// Sending report
$('#report_form').submit(function (event) {
    event.preventDefault();
    $('#reportModal').modal('hide') // Hiding modal

    let reportText = $('#report_text')

    //Forming dict with data
    let data = {
        text: reportText.val(),
        task: getCurrentTask()
    }

    reportText.val('') // Clearing textarea

    // Sending AJAX
    $.ajax({
        type: 'POST',
        url: '/api/send_report',
        contentType: 'application/json;charset=UTF-8',
        data: JSON.stringify(data),
        success: function (response) {
            console.log(response);
        },
        error: function (error) {
            console.log(error);
        }
    });
})