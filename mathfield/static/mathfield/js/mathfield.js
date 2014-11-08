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
        var data;
        data = JSON.parse(rawInput);
        //textarea.val(data['raw']);
        alert(compileLaTeX(data['raw']));
    }

    /* pass compileLaTeX a string of text. LaTeX should be surrounded by dollar
     * signs ($). Text outside of $s will be rendered as normal text. Dollar
     * signs preceeded by backslashes (\) will be rendered as normal dollar
     * signs. This function is a JS adaptation of mathfield.api.get_math.
     * RETURNS: compiled HTML
     */
    function compileLaTeX(rawstring){
        if(!rawstring){
            return rawstring
        }
        var reg = /(^|[^\\])\$(([^\$]|\\\$)*[^\\])\$/g;
        var match = reg.exec(rawstring);
        var returnlist = [];
        var loc = 0;
        while(match){
            var rawMath = match[2];
            // the raw math will be surrounded by $ characters, which need to be
            // removed. Since JS doesn't support negative lookbehinds in regex,
            // the first character of the string will be the character before
            // the $, unless it occurred at the beginning of the string. That
            // needs to be removed too.
            var mathStart = match['index'];
            if(match[0][0] !== '$'){
                mathStart += 1;
            }
            var prestring = rawstring.slice(loc, mathStart);
            prestring = prestring.replace('\\$', '$');
            returnlist.push(prestring);

            rawMath = rawMath.replace('\\$', '\\$ ');
            var html = katex.renderToString(rawMath);
            html = html.replace('\\$ ', '$')
            returnlist.push(html);

            loc += rawMath.length + 2;
            match = reg.exec(rawstring);
        }
        returnlist.push(rawstring.slice(loc, rawstring.length));
        return returnlist.join('');
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