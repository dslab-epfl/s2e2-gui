from __future__ import unicode_literals

from django.db import models

class PluginConfig():
	def __init__(self, plugin_name, plugin_descr, list_plugin_attr):
		self.plugin_name = plugin_name
		self.plugin_descr = plugin_descr
		self.list_plugin_attr = list_plugin_attr


class Attribute():
	def __init__(self, attr_name, attr_descr, attr_type):
		self.attr_name = attr_name
		self.attr_descr = attr_descr
		self.attr_type = attr_type


