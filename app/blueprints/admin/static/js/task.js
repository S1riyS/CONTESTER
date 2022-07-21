import {showAlert} from "../../../../static/js/modules/alert.js";

let grade_select = $('#grade');
let topic_select = $('#topic');
let testBlockList = $('#all_tests')
let currentTestID = 1;
let testsCounter = 1;

// Renders single option tag
function renderOption(topic) {
    return '<option value="' + topic.id + '">' + topic.name + '</option>';
}

// Renders new options of topic select field
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
                for (let topic of response.topics) {
                    options += renderOption(topic);
                }
            } else {
                topic_select.addClass('empty-dropdown')
            }

            topic_select.html(options);
        },
        error: function (error) {
            showAlert('Что-то пошло не так', 'danger');
        }
    })
})

// Creates new test block
$('#createNewTest').click(function () {
    event.preventDefault();
    currentTestID += 1;
    testsCounter += 1;
    let testBlockHTML = `<div class="create_task__test_block">
                                <div class="test_block__body">
                                    <div class="input_block">
                                        <p class="input_block__title">Ввод:</p>
                                        <textarea class="input_field auto_expand" id="tests-${currentTestID}-stdin"
                                         name="tests-${currentTestID}-stdin" placeholder="Ввод" required="" type="text"></textarea>
                                    </div>
                                    <div class="input_block">
                                        <p class="input_block__title">Вывод:</p>
                                        <textarea class="input_field auto_expand" id="tests-${currentTestID}-stdin" 
                                        name="tests-${currentTestID}-stdin" placeholder="Вывод" required="" type="text"></textarea>
                                    </div>
                                </div>

                                <div class="test_block__footer">
                                    <div class="footer__left">
                                        <div class="is_hidden check">
                                            <input checked id="tests-0-is_hidden" name="tests-${currentTestID}-is_hidden" 
                                            type="checkbox" value="y">
                                        </div>
                                        <label for="is_test_hidden_" class="is_hidden__label">
                                            Скрыть тест
                                        </label>
                                    </div>
                                    <div class="footer__right">
                                        <button title="Удалить тест" class="alert_button delete_test__button" type="button">
                                            <i class="default_button__icon far fa-trash-alt" aria-hidden="true"></i>
                                        </button>
                                    </div>
                                </div>
                            </div>`
    testBlockList.append(testBlockHTML);
})

// Deletes task block
$(document).on('click', '.delete_test__button', function () {
    if (testsCounter !== 1) {
        let testBlock = $(this).closest('.create_task__test_block')
        testBlock.remove();
        testsCounter -= 1;
    }
})

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

// Creates task
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
