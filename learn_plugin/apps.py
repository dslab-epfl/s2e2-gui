from __future__ import unicode_literals

from django.apps import AppConfig
from models import S2ECodeParser


class LearnPluginConfig(AppConfig):
    name = 'learn_plugin'
    
    def ready(self):
        S2ECodeParser.parsePlugin("/home/davide/S2E/s2e/qemu/s2e/Plugins/Debugger.cpp")
        #S2ECodeParser.parseCode("/home/davide/S2E/python/test.cpp")
 