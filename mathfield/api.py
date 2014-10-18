import subprocess
import os
import re

# These are functions for developers to use externally

def get_math(raw='', html=''):
    """ MathFields must be stored in the database as a string containing both
        the raw math and html.

        Arguments:

        * raw: this is your raw math as either Python math, LaTeX, or just
                     regular text

        * html: if you already know the html, there's no sense in calculating it
                again! But if you don't know it, leave this one blank and it 
                will be done for you.

        Returns:

        * dictionary with keys 'raw' and 'html'

        NOTICES:

        * Blocks of math must be enclosed in dollar signs. This is true whether
          your math is LaTeX or Python math. If you need the normal dollar 
          signs, use dollar signs proceeded by backslashes, `\$`.

        * NODE.JS MUST BE INSTALLED FOR THIS FUNCTION TO RUN
    """
    if raw == '' or html != '':
        return {'raw': raw, 'html': html}

    reg = re.finditer(r"(^|(?<!\\))\$(([^\$]|\\\$)*[^\\])\$", raw)

    # generate_html.js must be passed all the math text ask command line args. 
    # The dollar signs get stripped in advanced because the shell will interpret 
    # those as variables. The program will return each math object separated by
    # newlines
    results = [(mat.start(2), mat.end(2), mat.group(2).strip()) 
                for mat in reg if mat]

    if results == []:
        return {'raw': raw, 'html': raw}

    math_start_positions, math_end_positions, raw_math = zip(*results)

    js_results = subprocess.check_output([
        'node', 
        os.path.join(os.path.dirname(__file__), 
            'generate_html.js')
        ] + list(raw_math)
    )
    html_bits = js_results.strip('\n').split('\n')

    final = []
    loc = 0
    for index, code in enumerate(html_bits):
        # measurements are one off from the index of the math to eliminate the
        # dollar sign specifiers
        final.append(raw[loc:math_start_positions[index]].strip('$'))
        final.append(code)
        loc = math_end_positions[index] + 1

    return {'raw': raw, 'html': ''.join(final)}
