# s2e2-gui
GUI for interacting with S2E2


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

6. Visit http://127.0.0.1:8000/ to access the GUI.

