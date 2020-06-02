// Entry point for the notebook bundle containing custom model definitions.
//
define(function() {
    "use strict";

    window['requirejs'].config({
        map: {
            '*': {
                '{{ cookiecutter.npm_package_name }}': 'nbextensions/{{ cookiecutter.python_package_name | replace("-","_")}}/index',
            },
        }
    });
    // Export the required load_ipython_extension function
    return {
        load_ipython_extension : function() {}
    };
});
