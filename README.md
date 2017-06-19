# S2E GUI

GUI for interacting with [S2E](http://s2e.systems).

Dependencies:
 - A working [S2E environment](https://github.com/s2e/s2e-env).
 - radare2

## Quick start

1. Add `display_all_analysis` and `configure_and_run_analysis` to your `INSTALLED_APPS` setting like this:

```python
    INSTALLED_APPS = [
        ...
        'configure_and_run_analysis',
        'display_all_analysis',
    ]
```

2. Include the `display_all_analysis` and `configure_and_run_analysis URLconf` in your `project urls.py` like this:

```python
    url(r'^display_all_analysis/', include('display_all_analysis.urls')),
    url(r'^', include('configure_and_run_analysis.urls')),
```

3. Set the `S2E_ENV_PATH` environment variable with the path of your S2E environment like this:

```
    S2E_ENV_PATH = "/path/to/your/s2e/environment/"
```

4. Run `python manage.py migrate` to create the database models.

5. Run your server with `python manage.py runserver`.

6. Browse to `http://<server>:8000/` to access the GUI.

## Plugin annotation:

A plugin annotation for this GUI is a comment in the code that starts with the tag `@s2e_plugin_option@`.
The body of the config option must follow the YAML format and is structured as follow:

```c
    // @s2e_plugin_option@
    // attribute_name:
    //   type: int
    //   description: "attribute description."
```

The type of the attribute can only be one of the following types:

- int
- bool
- string
- stringList
- intList
- list

The list type has a different construct; instead of `attribute_name` you must specify a prefix allong with the
`content` tag.

Here is an example of a list starting with the prefix `list_prefix` and containing a boolean named `checked`:

```c
    // list_prefix:
    //   type: list
    //   description: "this is the description of the list"
    //   content:
    //     checked:
    //       type: bool
    //       description: "this is the description of checked"
```
