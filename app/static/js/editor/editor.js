import {getCurrentTask} from "../modules/current_task.js";

$(document).ready(function () {
    let languages = $('.dropdown-menu').closest('.dropdown-menu').find('a');
    let currentLanguage = localStorage.getItem('currentLanguage');
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
    let codeMirrorText = localStorage.getItem('codeMirrorText');
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
        localStorage.setItem('codeMirrorText', myCodeMirror.getValue())
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
    let dropdownMenuText = $('#dropdownBtn__text')
    myCodeMirror.setOption("mode", currentLanguage.dataset.mode)

    // Setting text
    dropdownMenuText.html(currentLanguage.text)

    // Saving current language to localStorage
    localStorage.setItem('currentLanguage', currentLanguage.dataset.value)
}


let myCodeMirror = loadCodeMirror(codeMirrorConfig) // Creating CodeMirror variable

// On click on "reset code" button
$('#reset-code__btn').click(function () {
    myCodeMirror.setValue('');
    myCodeMirror.focus();
    myCodeMirror.setCursor({line: 1, ch: 1});
})

// ON click on "copy code" button
function copyToClipboard(str) {
    let area = document.createElement('textarea');

    document.body.appendChild(area);
    area.value = str;
    area.select();
    document.execCommand("copy");
    document.body.removeChild(area);
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
        let language = getCurrentLanguage();
        let request = {
            code: myCodeMirror.getValue(),
            lang: language.dataset.value,
            task: getCurrentTask()
        };

        let codeResponse = $('#code-response__body')
        let codeResponseLoader = $('#code-response__loader')

        // Sending AJAX request to server
        $.ajax({
            url: '/api/send_code',
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
                codeResponse.replaceWith(response) // setting generated HTML
                scrollTo($('#code-response__body')) // Scrolling to response
            },
            // Error
            error: function () {
                console.log('Error')
            }
        })
    }
})

// On dropdown child click do...
$(".dropdown-menu a").click(function () {
    // Remove any existing 'active' classes...
    $(this).closest('.dropdown-menu').find('a').removeClass('active');

    // Add 'active' class to clicked element...
    $(this).addClass('active');

    // Setting language
    setLanguage($(this))
});