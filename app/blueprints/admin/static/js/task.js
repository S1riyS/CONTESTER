import {showAlert} from "../../../../static/js/modules/alert.js";

let grade_select = $('#grade')
let topic_select = $('#topic')

grade_select.change(function () {
    let grade_id = grade_select.val();

    $.ajax({
        type: 'POST',
        url: '/api/topics',
        contentType: 'application/json;charset=UTF-8',
        data: JSON.stringify({
            grade_id: grade_id
        }),
        success: function (response) {
            let options = '';

            if (response.topics.length !== 0) {
                topic_select.removeClass('empty-dropdown')
                topic_select.removeAttr('disabled');
                for (let topic of response.topics) {
                    options += renderOption(topic);
                }
            } else {
                topic_select.addClass('empty-dropdown')
                topic_select.attr('disabled','disabled');
            }

            topic_select.html(options);
        },
        error: function (error) {
            showAlert('Что-то пошло не так', 'danger');
        }
    })
})


function renderOption(topic) {
    return '<option value="' + topic.id + '">' + topic.name + '</option>';
}

let current_test = 1

function createTestBlock() {
    let request = {
        test_number: current_test
    }
    console.log(JSON.stringify(request))

    $.ajax({
        type: 'POST',
        url: '/api/admin/test_block',
        contentType: 'application/json;charset=UTF-8',
        data: JSON.stringify(request),
        success: function (response) {
            $('#all_tests').append(response)
        },
        error: function (error) {
            console.log(error);
        }
    })

    current_test += 1;
}

function getTests() {
    let inputsArray = [],
        outputsArray = [],
        checkboxesArray = []

    $("textarea[name='test_inputs[]']").each(function () {
        inputsArray.push($(this).val())
    })

    $("textarea[name='test_outputs[]']").each(function () {
        outputsArray.push($(this).val())
    })

    $(".task__is_hidden").each(function () {
        checkboxesArray.push($(this).is(':checked'))
    })

    return {
        inputs: inputsArray,
        outputs: outputsArray,
        is_hidden: checkboxesArray
    }
}

$("#task_from").submit(function (event) {
    event.preventDefault();
    let grade_id = $('#dropdownMenuGrade .dropdown-item.active').data('value');
    let topic_id = $('#dropdownMenuTopic .dropdown-item.active').data('value')

    if (grade_id && topic_id) {
        let request = {
            path: {
                grade_id: grade_id,
                topic_id: topic_id,
            },
            information: {
                name: $('#task__name').val(),
                condition: $('#task__condition').val()
            },
            example: {
                input: $('#task__input').val(),
                output: $('#task__output').val()
            },
            tests: getTests()
        }

        $.ajax({
            type: 'POST',
            url: '/api/admin/task',
            contentType: 'application/json;charset=UTF-8',
            data: JSON.stringify(request),
            success: function (response) {
                let type;

                if (response['success']) {
                    type = 'success'
                } else {
                    type = 'danger'
                }
                showAlert(response['message'], type);
            },
            error: function (error) {
                showAlert('Что-то пошло не так', 'danger');
            }
        });
    }
});

$('#create_test_button').click(function () {
    event.preventDefault();
    createTestBlock();
})

$(document).on('click', '.delete_test__button', function () {
    let testBlock = $(this).closest('.create_task__test_block')
    testBlock.remove();
})


$(document).ready(function () {
    createTestBlock()
})
