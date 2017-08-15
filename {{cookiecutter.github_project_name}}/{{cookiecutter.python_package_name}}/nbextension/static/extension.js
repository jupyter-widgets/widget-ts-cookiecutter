define(function() {
    "use strict";

    window['requirejs'].config({
        map: {
            '*': {
                '{{ cookiecutter.npm_package_name }}': 'nbextensions/{{ cookiecutter.npm_package_name }}/index',
            },
        }
    });
    // Export the required load_ipython_extention
    return {
        load_ipython_extension : function() {}
    };
});
