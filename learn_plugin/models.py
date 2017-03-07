from __future__ import unicode_literals
from __future__ import print_function

from django.db import models
import clang.cindex
import sys
from types import NoneType
from __builtin__ import staticmethod, True
import yaml 


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
		
		
class S2ECodeParser():
	CONFIG_TAG = "@s2e_plugin_option@"
	
	
	@staticmethod
	def parsePlugin(filePath):
		index = clang.cindex.Index.create()
		tu = index.parse(filePath)
		print('Translation unit:', tu.spelling)
		
		pluginDescription = S2ECodeParser.tokenListToString(S2ECodeParser.getPluginDescription(tu.cursor))
		
		S2ECodeParser.getNextConfigOption(tu.cursor.get_tokens())
		
		
	@staticmethod
	def iterateChildren(cursor, level = 0):
		for c in cursor.get_children():
			#if(check == False or c.spelling == head):				
			if(c.location.line == 26):
				print(S2ECodeParser.levelToString(level) + "display : " + c.displayname)
				print(S2ECodeParser.levelToString(level) + "kind : " + str(c.kind))
				print(S2ECodeParser.levelToString(level) + "location : " + str(c.location))
				print(S2ECodeParser.levelToString(level) + "spelling : " + str(c.spelling))
				print(S2ECodeParser.levelToString(level) + "display : " + c.displayname)
				print("\n")
				
			S2ECodeParser.iterateChildren(c, level + 1)
			
	@staticmethod
	def getPluginDescription(cursor):
		generator = cursor.get_tokens()
		notFound = True
		while(notFound):
			try:
				currentToken = next(generator)
					
				# check for the plugin definition
				if(currentToken.spelling == "S2E_DEFINE_PLUGIN"):
					if(next(generator).spelling == "("):
						return S2ECodeParser.getTokenFromTo((S2ECodeParser.getUpToCloseParenthesis(generator)), ',', ',')
						
			except StopIteration:
				return IOError("can't find the plugin description")
	
	@staticmethod
	def getAllConfigOption(cursor):
		generator = cursor.get_tokens()
		while(getNextConfigOption != None):
			pass
		
				
	
	@staticmethod
	def getNextConfigOption(generator):
		'''Finds the next config option tag'''
		notFound = True
		while(notFound):
			try:
				currentToken = next(generator)
					
				#TODO look for the comment done like this : /* */ 
				#looks for the plugin config option (multiline comment with "//")
				currentTokenSpelling = currentToken.spelling.decode("utf-8")
				if(currentTokenSpelling.startswith("//") and currentTokenSpelling.find(S2ECodeParser.CONFIG_TAG) != -1):
					configOptionString = ""
					currentToken = next(generator)
					currentTokenSpelling = currentToken.spelling.decode("utf-8")
					while(currentTokenSpelling.startswith("//")):
						configOptionString = configOptionString + currentTokenSpelling[2:] + "\n"
						
						currentToken = next(generator)
						currentTokenSpelling = currentToken.spelling.decode("utf-8")
						
					print(yaml.safe_load(configOptionString))
						
						
			except StopIteration:
				return None
	
	@staticmethod
	def getTokenFromTo(tokenList, matchFrom, matchTo):
		outputList = []
		hasMatch = False
		for token in tokenList:
			if(hasMatch and token.spelling == matchTo):
				return outputList
			if(hasMatch == True):
				outputList.append(token)
			if(token.spelling == matchFrom):
				hasMatch = True
			
	
	@staticmethod
	def iterateToken(cursor):
		
		#Detect the list of following string
		#toFind = ["s2e", "(", ")", "->", "getConfig", "(", ")", "->", None, "("]
		#toFindPos8 = ["getInt", "getBool"]
		toFind = ["S2E_DEFINE_PLUGIN"]
		toFindPos = 0
		currentToken = ""
		generator = cursor.get_tokens()
		hasNext = True
		
		while(hasNext):
			try:
				currentToken = next(generator)
					
				# if we found the next element in the list or if it is the item in the 8th positions
				if((currentToken.spelling == toFind[toFindPos]) or (toFindPos == 8 and currentToken.spelling in toFindPos8)):
					toFindPos = toFindPos + 1
					if(toFindPos == len(toFind)):	
						toFindPos = 0
						print(next(generator).spelling)
						print(next(generator).spelling)
						print(next(generator).spelling)
						print(next(generator).spelling)
						print(next(generator).spelling)
						#S2ECodeParser.printToken(S2ECodeParser.getUpToCloseParenthesis(generator))
				else:
					toFindPos = 0
					
			except StopIteration:
				hasNext = False
		
			
	@staticmethod
	def printToken(tokenList):
		for token in tokenList:
			print(token.spelling, end='')	
		print("\n")
		
	@staticmethod
	def tokenListToString(tokenList):
		outPutString = ""
		for token in tokenList:
			outPutString = outPutString + token.spelling
		return outPutString
		
	@staticmethod
	def getUpToCloseParenthesis(generator):
		outputList = list()
		currentToken = None
		currentLevel = 1
		while(True):
			try:
				currentToken = next(generator)
			except StopIteration:
				#TODO add plugin name and make more robust
				print("Cannot generate config file for the plugin : ")
				return
			
			outputList.append(currentToken)
			
			if(currentToken.spelling == "("):
				currentLevel = currentLevel + 1
			elif(currentToken.spelling == ")"):
				currentLevel = currentLevel - 1
				if(currentLevel == 0):
					break
			
			
		del outputList[-1]	
		return outputList
        
	@staticmethod
	def levelToString(level):
		out = ""
		for x in range(level):
			out = out + "-"
		return out
	
# 	@staticmethod
# 	def find_typerefs(node, typename):
# 		""" Find all references to the type named 'typename'
# 		"""
# 		if node.kind.is_reference():
# 			ref_node = node.get_definition()
# 			if(type(ref_node) != NoneType):
# 				if ref_node.spelling == typename:
# 					print 'Found %s [line=%s, col=%s]' % (
# 						typename, node.location.line, node.location.column)
# 		
# 		# Recurse for children of this node
# 		for c in node.get_children():
# 			S2ECodeParser.find_typerefs(c, typename)
		


