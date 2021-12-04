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

function getCurrentPath() {
    let path = window.location.pathname.split('/');
    return {
        grade: path[1],
        topic: path[2],
        task_number: path[3]
    }
}

function getCurrentLanguage() {
    return language = $('#dropdownMenuLanguage').find('.active')[0];
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


myCodeMirror = loadCodeMirror(codeMirrorConfig) // Creating CodeMirror variable

// On click on "reset code" button
$('#reset-code__btn').click(function () {
    myCodeMirror.setValue('');
    myCodeMirror.focus();
    myCodeMirror.setCursor({line: 1, ch: 1});
})

// On click on "submit" button
$('#submit-code__btn').click(function () {
    let language = getCurrentLanguage();

    // Collecting request
    let request = {
        code: myCodeMirror.getValue(),
        lang: language.dataset.value,
        task: getCurrentPath()
    };

    // Sending AJAX request to server
    let codeResponse = $('#code-response')
    $.ajax({
        url: '/api/send_code',
        type: 'POST',
        contentType: 'application/json;charset=UTF-8',
        data: JSON.stringify(request),
        // Before send
        beforeSend: function () {
            codeResponse.html('');
        },
        // Success
        success: function (response) {
            codeResponse.replaceWith(response) // setting generated HTML

            // Scrolling to response
            scrollTo($('#code-response'))
        },
        // Error
        error: function () {
            console.log('Error')
        }
    })
})

// On dropdown child click do...
$(".dropdown-menu a").click(function () {
    // Remove any existing 'active' classes...
    $(this).closest('.dropdown-menu').find('a').removeClass('active');
    // Add 'active' class to clicked element...
    $(this).addClass('active');

    // Setting chosen language mode to CodeMirror
    let currentLanguage = $(this)[0]
    let dropdownMenuText = $('#dropdownBtn__text')
    myCodeMirror.setOption("mode", currentLanguage.dataset.mode)
    dropdownMenuText.html(currentLanguage.text)
});