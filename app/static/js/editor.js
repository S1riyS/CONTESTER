import {getCurrentTask} from "./modules/current_task.js";
import {showAlert} from "./modules/alert.js";

function loadTaskToLocalStorage() {
    let taskStorage = localStorage.getItem('taskStorage', null);

    if (taskStorage === null) {
        localStorage.setItem('taskStorage', JSON.stringify({}));
    }

    taskStorage = JSON.parse(localStorage.getItem('taskStorage'));

    if (!taskStorage[location.pathname]) {
        taskStorage[location.pathname] = {'language': null, 'source_code': null}
        localStorage.setItem('taskStorage', JSON.stringify(taskStorage));
    }
}

$(document).ready(function () {
    let languages = $('.dropdown-menu').closest('.dropdown-menu').find('a');

    loadTaskToLocalStorage()
    let taskStorage = JSON.parse(localStorage.getItem('taskStorage'));
    let currentLanguage = taskStorage[location.pathname]['language'];

    languages.each(function () {
        // Remove any existing 'active' classes...
        if ($(this)[0].dataset.value === currentLanguage) {
            languages.removeClass('active');

            // Add 'active' class to clicked element...
            $(this).addClass('active');

            // Setting language
            setLanguage($(this))
        }
    })
});

let codeMirrorConfig = {
    mode: "text/x-pascal", // Language mode
    theme: "material-palenight", // theme
    lineNumbers: true, // set number
    smartIndent: true, // smart indent
    indentUnit: 4, // Smart indent in 4 spaces
    indentWithTabs: true, // Smart indent with tabs
    lineWrapping: true, //
    // Add line number display, folder and syntax detector to the slot
    gutters: ["CodeMirror-linenumbers", "CodeMirror-foldgutter", "CodeMirror-lint-markers"],
    foldGutter: true, // Enable code folding in slots
    autofocus: true, // Autofocus
    matchBrackets: true, // Match end symbols, such as "],}"
    autoCloseBrackets: true, // Auto close symbol
    styleActiveLine: true, // Display the style of the selected row
    scrollbarStyle: 'simple' // Scrollbar style
}

function getCurrentLanguage() {
    return $('#dropdownMenuLanguage').find('.active')[0];
}

function loadCodeMirror(config) {
    // Configuring CodeMirror
    let editor = document.getElementById("editor__body");
    let myCodeMirror = CodeMirror(editor, config);

    // Loading code from local storage
    let initEditorValue;

    loadTaskToLocalStorage();
    let taskStorage = JSON.parse(localStorage.getItem('taskStorage'));
    let codeMirrorText = taskStorage[location.pathname]['source_code'];

    if (codeMirrorText) {
        initEditorValue = codeMirrorText
    } else {
        initEditorValue = ''
    }
    // Setting saved code
    myCodeMirror.setValue(initEditorValue);

    // Setting current mode
    let currentLanguage = getCurrentLanguage()
    myCodeMirror.setOption('mode', currentLanguage.dataset.mode)

    // Saving code everytime it changes
    myCodeMirror.on('change', function () {
        let taskStorage = JSON.parse(localStorage.getItem('taskStorage'));
        taskStorage[location.pathname]['source_code'] = myCodeMirror.getValue();
        localStorage.setItem('taskStorage', JSON.stringify(taskStorage));
    })

    return myCodeMirror
}

function scrollTo(obj) {
    // Scrolling
    $('html, body').animate({
        scrollTop: obj.offset().top
    });
}

function setLanguage(language) {
    // Setting chosen language mode to CodeMirror
    let currentLanguage = language[0]
    let dropdownMenuText = $('#languageDropdownButton__text')
    myCodeMirror.setOption("mode", currentLanguage.dataset.mode)

    // Setting text
    dropdownMenuText.html(currentLanguage.text)

    // Saving current language to localStorage
    let taskStorage = JSON.parse(localStorage.getItem('taskStorage'));
    taskStorage[location.pathname]['language'] = currentLanguage.dataset.value;
    localStorage.setItem('taskStorage', JSON.stringify(taskStorage));
}

let myCodeMirror = loadCodeMirror(codeMirrorConfig) // Creating CodeMirror variable

// On click on "reset code" button
$('#reset-code__btn').click(function () {
    myCodeMirror.setValue('');
    myCodeMirror.focus();
    myCodeMirror.setCursor({line: 1, ch: 1});

    showAlert('Код удален', 'danger')
})

// ON click on "copy code" button
function copyToClipboard(str) {
    let area = document.createElement('textarea');

    document.body.appendChild(area);
    area.value = str;
    area.select();
    document.execCommand("copy");
    document.body.removeChild(area);

    showAlert('Код скопирован', 'info')
}

$('#copy-code__btn').click(function () {
    copyToClipboard(myCodeMirror.getValue())
})

let isRequestInProgress = false;
// On click on "submit" button
$('#submit-code__btn').click(function () {
    if (!isRequestInProgress) {
        let submitCodeButton = $('#submit-code__btn')

        // Collecting request
        let partner_id = $('#dropdownMenuClassmate .dropdown-item.active').data('id') || null
        let language = getCurrentLanguage();
        let request = {
            code: myCodeMirror.getValue(),
            lang: language.dataset.value,
            path: getCurrentTask(),
            partner_id: partner_id
        };

        let codeResponse = $('#code-response__body')
        let codeResponseLoader = $('#code-response__loader')

        // Sending AJAX request to server
        $.ajax({
            url: '/api/task/solution',
            type: 'POST',
            contentType: 'application/json;charset=UTF-8',
            data: JSON.stringify(request),
            // Before send
            beforeSend: function () {
                codeResponse.html('');
                isRequestInProgress = true;
                submitCodeButton.prop("disabled", true);
                codeResponseLoader.css({'display': 'block'});
                scrollTo(codeResponseLoader);
            },
            // Complete
            complete: function () {
                isRequestInProgress = false;
                submitCodeButton.prop("disabled", false);
                codeResponseLoader.css({'display': 'none'});
            },
            // Success
            success: function (response) {
                codeResponse.replaceWith(response['result']) // setting generated HTML
                scrollTo($('#code-response__body')) // Scrolling to response
            },
            // Error
            error: function () {
                showAlert('Что-то пошло не так', 'danger');
            }
        })
    }
})

// On dropdown child click do...
$("#dropdownMenuLanguage a").click(function () {
    $(this).closest('.dropdown-menu').find('a').removeClass('active');
    $(this).addClass('active');
    // Setting language
    setLanguage($(this))
});


// On dropdown child click do...
$("#dropdownMenuClassmate a").click(function () {
    $(this).closest('.dropdown-menu').find('a').removeClass('active');
    $(this).addClass('active');
    let dropdownMenuText = $('#classmateDropdownButton__text');
    let classmate = $(this)[0]
    dropdownMenuText.html(classmate.dataset.fullname)
});