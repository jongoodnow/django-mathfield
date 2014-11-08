(function($){

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

    /* get the selector of the input */
    function getInput(textareaID){
        return $('textarea#' + textareaID);
    }

    /* get the selector of the containing div of the mathfield textarea input */
    function getContainer(textareaID){
        return $('div#' + textareaID + '-container');
    }

    /* get the selector of preview span next to the mathfeild textarea input */
    function getPreview(textareaID){
        return $('span#' + textareaID + '-preview');
    }

    /* renderMathFieldForm is called directly after the form is created.
     * This is only called automatically if the MathFieldWidget is specified
     * for the field. Otherwise it must be called manually. If you are calling
     * manually, make sure that the widget you are using using a textarea input
     */
    this.renderMathFieldForm = function(textareaID, rawtext, html){
        var textarea = getInput(textareaID);
        textarea.addClass('mathfield-latexform');
        var container = getContainer(textareaID);
        // the input initially shows the JSON. Make it just show the raw text.
        textarea.val(rawtext);

        // add the preview next to the text area
        container.append('<span id="' + textareaID + '-preview" style="border: '
            + '1px solid #CCC; width: ' + textarea.width() + 'px; height:' 
            + textarea.height() + 'px; display: inline-block; margin: 2px'
            + ' 10px; padding: 2px; overflow-y: scroll; word-wrap: break-word;"'
            + '></span>');

        var preview = getPreview(textareaID);
        preview.html(html);
    }

    $(document).ready(function(){

        $('.mathfield-latexform').keyup(function(event){
            var id = event.target.id;
            var textarea = getInput(id);
            var preview = getPreview(id);
            var latex = textarea.val();
            var html = compileLaTeX(latex);
            preview.html(html);
        }).change();

    });

})(django.jQuery);