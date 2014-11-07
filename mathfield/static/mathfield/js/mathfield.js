(function($){

    /* The form input contains both the raw LaTeX and the compiled HTML.
     * it should be modified so that it only shows the LaTeX, while the HTML
     * is rendered in an adjacent preview span.
     */
    function parseJSONFromForm(textareaID){
        var textarea = $('textarea#' + textareaID);
        var rawInput = textarea.val();
        if(!rawInput){
            return // there's nothing there yet
        }
        try{
            var data = JSON.parse(rawInput);
        }
        catch(err){
            // if the string cannot be parsed as JSON, then it is likely
            // just a string of latex, so it should be rendered now
        }
        textarea.val(data['raw']);

    }

    /* pass compileLaTeX a string of text. LaTeX should be surrounded by dollar
     * signs ($). Text outside of $s will be rendered as normal text. Dollar
     * signs preceeded by backslashes (\) will be rendered as normal dollar
     * signs. This function is a JS adaptation of mathfield.api.get_math.
     */
    function compileLaTeX(rawstring){

    }

    /* renderMathFieldForm is called directly after the form is created.
     * This is only called automatically if the MathFieldWidget is specified
     * for the field. Otherwise it must be called manually. If you are calling
     * manually, make sure that the widget you are using using a textarea input
     */
    this.renderMathFieldForm = function(textareaID){
        parseJSONFromForm(textareaID);
    }

})(django.jQuery);