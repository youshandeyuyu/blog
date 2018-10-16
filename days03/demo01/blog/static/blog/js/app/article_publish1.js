var testEditor;

    $(function() {
        testEditor = editormd("test-editormd", {
            width   : "100%",
            height  : 640,
            syncScrolling : "single",
            path    : "/static/js/lib/editor.md-master/lib/"
        });

    });