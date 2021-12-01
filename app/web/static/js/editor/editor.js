// Loading CodeMirror editor
window.onload = function () {
    let editor = document.getElementById("editor__body");
    let myCodeMirror = CodeMirror(editor, {
        mode: "python", // Language mode
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

    });
};
