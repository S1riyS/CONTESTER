let current_test = 1

function createTestBlock() {
    let request = {
        test_number: current_test
    }

    $.ajax({
        type: 'POST',
        url: '/api/get_task_input_block',
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
        inputsArray: inputsArray,
        outputsArray: outputsArray,
        checkboxesArray: checkboxesArray
    }
}

$("#task_from").submit(function (event) {
    event.preventDefault();

    let request = {
        path: {
            grade: $('#dropdown_grade__text').val(),
            topic: $('#dropdown_topic__text').val(),

        },
        basic_information: {
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
        url: '/api/create_task',
        contentType: 'application/json;charset=UTF-8',
        data: JSON.stringify(request),
        success: function (response) {
            console.log(response);
        },
        error: function (error) {
            console.log(error);
        }
    });
});

$('#create_test_button').click(function () {
    event.preventDefault();
    createTestBlock();
})

$(document).on('click', '.delete_test__button', function () {
    let testBlock = $(this).closest('.create_task__test_block')
    testBlock.remove();
})

// On dropdown child click do...
$(".dropdown-menu a").click(function () {
    // Remove any existing 'active' classes...
    $(this).closest('.dropdown-menu').find('a').removeClass('active');

    // Add 'active' class to clicked element...
    $(this).addClass('active');

    // Setting language
    // setLanguage($(this))
});

$(document).ready(function () {
    createTestBlock()
})
