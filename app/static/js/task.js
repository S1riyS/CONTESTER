import {getCurrentTask} from "./modules/current_task.js";

let currentSidebarY = -1;

function setScrollBarAttributes() {
    let sidebar = $('#sidebar');
    let taskMain = $('#task__main');

    if (currentSidebarY <= 0) currentSidebarY = findPosY(sidebar);

    if (pageYOffset > 70) {
        sidebar.addClass('fixed_position')
        sidebar.removeClass('default_position')
        taskMain.addClass("offset-xl-2");
    } else {
        sidebar.addClass('default_position')
        sidebar.removeClass('fixed_position')
        taskMain.removeClass("offset-xl-2");
    }
}

function findPosY(obj) {
    let offset = obj.offset()
    return offset.top - $(window).scrollTop()
}

function setActiveTab() {
    let activeTabs = window.localStorage.getItem('activeTab');

    if (activeTabs) {
        let activeTabs = (window.localStorage.getItem('activeTab') ? window.localStorage.getItem('activeTab').split(',') : []);
        $.each(activeTabs, function (index, element) {
            $('[data-toggle="tab"][href="' + element + '"]').tab('show');
        });
    }
}

function hideSeparators(tabs) {
    $('#task_tabs .nav-link').removeClass('hide_after')

    $(tabs).each(function () {
        $(this).addClass('hide_after')
    })
}

// Hiding tabs separators, setting attributes to scrollbar (on load)
window.onload = function () {
    setActiveTab();
    let activeTab = $('#task_tabs .nav-link.active').first();
    let nextAfterActiveTab = activeTab.parent().next('.nav-item').children('.nav-link');
    hideSeparators([activeTab, nextAfterActiveTab]);
    setScrollBarAttributes();
    $(".loader_wrapper").fadeOut("slow");
}

// Setting attributes to scrollbar (on scroll)
$(window).scroll(function () {
    setScrollBarAttributes()
});

// Tabs events
$('a[data-toggle="tab"]')
    .on('shown.bs.tab', function (e) {
        let currentTab = $(this)
        let nextTab = $(this).parent().next('.nav-item').children('.nav-link')
        hideSeparators([currentTab, nextTab])
    })
    .on('click', function (e) {

        let theTabId = $(this).attr('href');
        let activeTabs = (window.localStorage.getItem('activeTab') ? window.localStorage.getItem('activeTab').split(',') : []);

        let $sameLevelTabs = $(e.target).parents('.nav-tabs').find('[data-toggle="tab"]');

        $.each($sameLevelTabs, function (index, element) {
            let tabId = $(element).attr('href');
            if (theTabId !== tabId && activeTabs.indexOf(tabId) !== -1) {
                activeTabs.splice(activeTabs.indexOf(tabId), 1);
            }
        });

        //unique tabs
        if (activeTabs.indexOf($(e.target).attr('href')) === -1) {
            activeTabs.push($(e.target).attr('href'));
        }

        window.localStorage.setItem('activeTab', activeTabs.join(','));

    });

// Get submissions tab
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

// Deleting task
$('#deleteTaskButton').on('click', function () {
    //Forming dict with data
    let data = {
        task: getCurrentTask()
    }

    $('#deleteModal').modal('hide') // Hiding modal

    // Sending AJAX
    $.ajax({
        type: 'POST',
        url: '/api/delete_task',
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
