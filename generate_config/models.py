from __future__ import unicode_literals

from django.db import models

CLASS_NORMAL = "normal"
CLASS_ERROR = "error"
CLASS_INSIDE_DIV = "inside"
CLASS_LIST_ELEMENT_DIV = "list_element"


class S2ELaunchException(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)
