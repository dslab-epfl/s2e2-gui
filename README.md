# s2e2-gui
GUI for interacting with S2E2



Plugin annotation:

A plugin annotation for this gui is a comment in the code that starts with the tag : "@s2e_plugin_option@".
The body of the config option must follow the YAML format and is structured as follow : 

// attribute_name:
//   type: int
//   description: "attribute description."

The type of the attribute can only be one of the following types : int, bool, string, stringList or list.

The list type has a different construct, instead of attribute_name, you must specify a prefix allong with the "content" tag.

Here is an example of a list starting with the prefix "list_prefix" and containing a boolean named "checked":

// list_prefix:
//   type: list
//   description: "this is the description of the list"
//   content: 
//     checked:
//       type: bool
//       description: "this is the description of checked
