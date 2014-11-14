// Generate HTML using KaTeX for use in django-mathfield and print to stdout
// This prints each command line argument as html, in the same order, separated
// by new lines

// node.js is required to run this file. It gets called by the python api, so no
// need to call it directly.

var katex = require('./static/mathfield/js/katex.min');

args = process.argv;

for(var i = 2; i < args.length; i++){
    var math = args[i];
    var html = katex.renderToString(math);

    // not using console.log because we don't want to print \r on Windows
    process.stdout.write(html + '\n');
}