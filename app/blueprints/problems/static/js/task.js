import {getCurrentTask} from "../../../../static/js/modules/current_task.js";
import {sendDefaultAjax, sendAjaxWithRedirect} from "../../../../static/js/modules/send_ajax.js";

let currentSidebarY = -1;

function setScrollBarAttributes() {
    let sidebar = $('#sidebar');
    let taskMain = $('#task__main');

    let headerHeight = $('#header').outerHeight();
    let confirmationHeight = $('#confirmation').outerHeight();

    if (typeof confirmationHeight === 'undefined') {
        confirmationHeight = 0
    }

    let offsetValue = headerHeight + confirmationHeight;

    if (currentSidebarY <= 0) currentSidebarY = findPosY(sidebar);

    if (pageYOffset > offsetValue) {
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

// Hiding tabs separators, setting attributes to scrollbar (on load)
window.onload = function () {
    setScrollBarAttributes();
    $(".loader_wrapper").fadeOut("slow");
}

// Setting attributes to scrollbar (on scroll)
$(window).scroll(function () {
    setScrollBarAttributes()
});

// Sending report
$('#report_form').submit(function (event) {
    event.preventDefault();
    $('#reportModal').modal('hide') // Hiding modal

    let reportText = $('#report_text')

    //Forming dict with data
    let data = {
        text: reportText.val(),
        path: getCurrentTask()
    }

    reportText.val('') // Clearing textarea

    sendDefaultAjax('POST', '/api/task/report', data)

})

// Deleting task
$('#deleteTaskButton').click(function () {
    console.log($(this).data())
    let data = {
        task_id: $(this)[0].dataset.taskid
    }

    $('#deleteModal').modal('hide') // Hiding modal

    sendAjaxWithRedirect('DELETE', '/api/admin/task', data)
})
