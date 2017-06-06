# s2e2-gui
GUI for interacting with S2E2

Dependencies: 
- s2e-env
- radare2
- django

Quick start
-----------

1. Add "display_all_analysis" and "configure_and_run_analysis" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'configure_and_run_analysis',
		'display_all_analysis',
    ]

2. Include the display_all_analysis and configure_and_run_analysis URLconf in your project urls.py like this::

	url(r'^display_all_analysis/', include('display_all_analysis.urls')),
	url(r'^', include('configure_and_run_analysis.urls')),

3. Add the variable S2E_ENVIRONEMENT_FOLDER_PATH with the path of your s2e environement like this:
	
	S2E_ENVIRONEMENT_FOLDER_PATH = "/path/to/your/s2e/environement/"

4. Run `python manage.py migrate` to create the database models.

5. Add your projects inside your environement folder to the statics files like this: 
	
	STATICFILES_DIRS = [
		...,
		"/path/to/your/s2e/environement/projects/",
		...,
	]

6. Run your server with `python manage runserver`

7. Visit http://127.0.0.1:8000/ to access the GUI.





Plugin annotation:
------------------

A plugin annotation for this gui is a comment in the code that starts with the tag : "@s2e_plugin_option@".
The body of the config option must follow the YAML format and is structured as follow : 

// @s2e_plugin_option@
// attribute_name:
//   type: int
//   description: "attribute description."

The type of the attribute can only be one of the following types : int, bool, string, stringList, intList or list.

The list type has a different construct, instead of attribute_name, you must specify a prefix allong with the "content" tag.

Here is an example of a list starting with the prefix "list_prefix" and containing a boolean named "checked":

// list_prefix:
//   type: list
//   description: "this is the description of the list"
//   content: 
//     checked:
//       type: bool
//       description: "this is the description of checked"
