from __future__ import unicode_literals

from django.apps import AppConfig
import clang.cindex
import sys

class LearnPluginConfig(AppConfig):
    name = 'learn_plugin'
    
    def find_typerefs(self, node, typename):
        """ Find all references to the type named 'typename'
        """
        if node.kind.is_reference():
            ref_node = node.get_definition()
            if ref_node.spelling == typename:
                print 'Found %s [line=%s, col=%s]' % (
                    typename, node.location.line, node.location.column)
        # Recurse for children of this node
        for c in node.get_children():
            self.find_typerefs(c, typename)
    
    def ready(self): 
        index = clang.cindex.Index.create()
        tu = index.parse("/home/davide/S2E/python/test.cpp")
        print 'Translation unit:', tu.spelling
        self.find_typerefs(tu.cursor, "Person")
    