# -*- coding: utf-8 -*-

import subprocess
import os
import re
import cgi
from django.utils.encoding import smart_unicode

# These are functions for developers to use externally

def store_math(raw='', html=''):
    """ MathFields must be stored in the database as a string containing both
        the raw math and html.

        Arguments:

        * raw: this is your raw math as either LaTeX or just regular text

        * html: if you already know the html, there's no sense in calculating it
                again! But if you don't know it, leave this one blank and it 
                will be done for you.

        Returns:

        * dictionary with keys 'raw' and 'html'

        NOTICES:

        * Blocks of math must be enclosed in dollar signs. 
          If you need the normal dollar signs, use dollar signs preceeded by 
          backslashes, `\$`.

        * NODE.JS MUST BE INSTALLED FOR THIS FUNCTION TO RUN
    """

    if raw == '' or html != '':
        return {'raw': raw, 'html': html}

    reg = re.finditer(r"(^|(?<!\\))\$(([^\$]|\\\$)*[^\\])\$", raw)

    # generate_html.js must be passed all the math text ask command line args. 
    # The dollar signs get stripped in advanced because the shell will interpret 
    # those as variables. The program will return each math object separated by
    # newlines. KaTeX doesn't understand actual dollar signs if they are
    # followed by another character (like x=\$2), so add a space after those
    results = [(mat.start(2), 
                mat.end(2), 
                mat.group(2).strip().replace('\\$', '\\$ ')
              ) for mat in reg if mat]

    if results == []:
        return {'raw': raw, 'html': raw}

    math_start_positions, math_end_positions, raw_math = zip(*results)

    # prepare the shell to get the LaTeX via a call to Node.js
    # the shell is not explicitly called so there's no danger of shell injection
    # The command `node` must be on the system path
    env = dict(os.environ)
    env['LC_ALL'] = 'en_US.UTF-8' # accept unicode characters as output
    p = subprocess.Popen([
        'node', 
        os.path.join(os.path.dirname(__file__), 'generate_html.js')] 
            + list(raw_math),
        env=env, 
        stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE)
    node_output, node_error = p.communicate()
    if node_error:
        raise NodeError(node_error)

    html_bits = node_output.strip('\n').split('\n')

    final = []
    loc = 0
    for index, code in enumerate(html_bits):
        # measurements are one off from the index of the math to eliminate the
        # dollar sign specifiers
        # KaTeX will handle HTML encoding for the math text, but regular text
        # must have HTML stripped out for security reasons.
        final.append(cgi.escape(raw[loc:math_start_positions[index]]
                        .strip('$').replace('\\$', '$')))
        final.append(smart_unicode(code))
        loc = math_end_positions[index] + 1

    final.append(cgi.escape(raw[loc:].replace('\\$', '$')))
    final_string = u''.join(final)

    return {'raw': raw, 'html': final_string}


class NodeError(Exception):
    pass