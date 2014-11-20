module.exports = function(grunt) {

    grunt.initConfig({
        pkg: grunt.file.readJSON('package.json'),
        uglify: {
            main: {
                files: {
                    'mathfield/static/mathfield/js/mathfield.min.js': [
                        'mathfield/static/mathfield/js/mathfield_admin.js',
                        'mathfield/static/mathfield/js/encoder.js',
                        'katex.min.js'
                    ]
                },
                options: {
                    banner: '/*! <%= pkg.name %> <%= grunt.template.today("dd-mm-yyyy") %> */\n',
                    sourceMap: 'mathfield/static/mathfield/js/mathfield.min.js.map',
                }
            },
        },
    });

    grunt.loadNpmTasks('grunt-contrib-uglify');

    grunt.registerTask('default', ['uglify']);

};