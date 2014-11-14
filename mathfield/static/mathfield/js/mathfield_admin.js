/*
 * JS for rendering the HTML LaTeX preview of django-mathfield in the Django 
 *   admin and submitting the rendered LaTeX to the DB.
 * Author: Jonathan Goodnow
 * Source: https://github.com/jongoodnow/django-mathfield
 * Licence: The BSD License
 * Copyright: (c) 2014 Jonathan Goodnow
 */

(function($){

    /* pass compileLaTeX a string of text. LaTeX should be surrounded by dollar
     * signs ($). Text outside of $s will be rendered as normal text. Dollar
     * signs preceeded by backslashes (\) will be rendered as normal dollar
     * signs. This function is a JS adaptation of mathfield.api.get_math.
     * RETURNS: compiled HTML
     */
    function compileLaTeX(rawstring){
        if(!rawstring){
            return rawstring;
        }
        var reg = /(^|[^\\])\$(([^\$]|\\\$)*[^\\])\$/g;
        var match = reg.exec(rawstring);
        var returnlist = [];
        var loc = 0;
        while(match){
            var rawMath = match[2];
            var mathlength = rawMath.length;
            // the raw math will be surrounded by $ characters, which need to be
            // removed. Since JS doesn't support negative lookbehinds in regex,
            // the first character of the string will be the character before
            // the $, unless it occurred at the beginning of the string. That
            // needs to be removed too.
            var mathStart = match.index;
            if(mathStart === 0){
                mathlength += 1;
            }
            else{
                mathStart += 1;
            }
            var prestring = rawstring.slice(loc, mathStart);
            prestring = prestring.replace('\\$', '$');
            prestring = Encoder.htmlEncode(prestring);
            returnlist.push(prestring);
            loc += prestring.length;

            rawMath = rawMath.replace('\\$', '\\$ ');
            var html = katex.renderToString(rawMath);
            html = html.replace('\\$ ', '$');
            returnlist.push(html);

            loc += match[1].length + mathlength + 1;
            match = reg.exec(rawstring);
        }
        returnlist.push(Encoder.htmlEncode(
            rawstring.slice(loc, rawstring.length)
        ));
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

    /* compile the LaTeX in a textarea and push it to the preview span */
    function updatePreview(textareaID){
        var textarea = getInput(textareaID);
        var preview = getPreview(textareaID);
        var latex = textarea.val();
        var html = compileLaTeX(latex);
        preview.html(html);
    }

    /* the size of the preview should match the size of the input. This resizes
     * the preview whenever the textarea is resized.
     */
    function resizePreview(textareaID) {
        var textarea = getInput(textareaID);
        var preview = getPreview(textareaID);
        var resizeInt = null;

        var resizeEvent = function() {
            preview.outerWidth(textarea.outerWidth());
            preview.outerHeight(textarea.outerHeight());
        };

        // firefox only
        textarea.on("mousedown", function(e) {
            resizeInt = setInterval(resizeEvent, 1000/15);
        });

        $(window).on("mouseup", function(e) {
            if (resizeInt !== null) {
                clearInterval(resizeInt);
            }
            resizeEvent();
        });
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
        textarea.val(Encoder.htmlDecode(rawtext));

        // add the preview next to the text area
        container.append(['<span id="', textareaID, '-preview" style="border: ',
            '1px solid #CCC; width: ', textarea.width(), 'px; height:',
            textarea.height(), 'px; display: inline-block; margin: 2px',
            ' 10px; padding: 2px; overflow-y: auto; word-wrap: break-word;"',
            '></span><span style="position: relative; left: -60px; bottom: ',
            '8px; color: #BBB;">Preview</span>'].join(''));

        var preview = getPreview(textareaID);
        preview.html(html);

        resizePreview(textareaID);
    };

    /* The form in the django admin wants valid JSON containing the raw LaTeX
     * and the HTML. For editing, the input contains only the LaTeX, so the
     * contents of the input must be modified before submitting.
     */
    this.serializeAndSubmit = function(){
        $('.mathfield-latexform').each(function(i, obj){
            var textarea = getInput(obj.id);
            var raw = textarea.val();
            var html = getPreview(obj.id).html();
            var ret = {
                "raw": raw,
                "html": html,
            };
            textarea.val(JSON.stringify(ret));
        });

        return false;
    };

    /* Listen for whenever the input is modified and when the form is submitted 
     */
    $(document).ready(function(){

        $('form').attr('onSubmit', 'javascript:serializeAndSubmit();');

        $('.mathfield-latexform').keyup(function(event){
            updatePreview(event.target.id);
        });

    });

})(django.jQuery);