from __future__ import unicode_literals
from __future__ import print_function

import clang.cindex
import os
from types import NoneType
from __builtin__ import staticmethod, True
import yaml 
import json
		
class PluginParseException(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)
		
class S2ECodeParser():
	CONFIG_TAG = "@s2e_plugin_option@"
	DESCRIPTION_TAG = "S2E_DEFINE_PLUGIN"
	
	
	@staticmethod
	def parseEveryPluginInDir(dirPath):
		everyPluginDict = []
		for root, dirs, files in os.walk(dirPath):
			for file in files:
				if(file.endswith(".cpp")):
					try:
						pluginDict = S2ECodeParser.parsePlugin(os.path.abspath(os.path.join(root, file)))
						everyPluginDict.append(pluginDict)
					except PluginParseException as e:
						print(e)
					
		with open("result.json", "w") as fp:
			json.dump(everyPluginDict, fp, indent=4, separators=(',', ': '))
		
		#S2ECodeParser.parsePlugin("/home/davide/S2E/s2e/qemu/s2e/Plugins/Debugger.cpp")
	
	@staticmethod
	def parsePlugin(filePath):
		index = clang.cindex.Index.create()
		tu = index.parse(filePath)
		print('Translation unit:', tu.spelling)
		
		pluginName, pluginDescr, pluginDep = S2ECodeParser.getPluginInfo(tu.cursor)
			
		configDictionary = S2ECodeParser.getAllConfigOption(tu.cursor)
		
		pluginDictionary = {}
		pluginDictionary["name"] = pluginName
		pluginDictionary["description"] = pluginDescr
		pluginDictionary["dependencies"] = pluginDep
		pluginDictionary["configOption"] = configDictionary
		
		return pluginDictionary
	
			
	@staticmethod
	def getPluginInfo(cursor):
		generator = cursor.get_tokens()
		notFound = True
		while(notFound):
			try:
				currentToken = next(generator)
					
				# check for the plugin definition
				if(currentToken.spelling == S2ECodeParser.DESCRIPTION_TAG):
					if(next(generator).spelling == "("):
						argumentList = S2ECodeParser.getArgumentList(S2ECodeParser.getUpToCloseParenthesis(generator), ',')
						return argumentList[0], argumentList[1], argumentList[3:]
						
			except StopIteration:
				raise PluginParseException("Can't find the plugin description")
	
	@staticmethod
	def getAllConfigOption(cursor):
		generator = cursor.get_tokens()
		configOut = {}
		nextConfig = S2ECodeParser.getNextConfigOption(generator)
		while(nextConfig != None):
			configOut = S2ECodeParser.mergeDictionary(configOut, nextConfig)
			nextConfig = S2ECodeParser.getNextConfigOption(generator)
		return configOut
				
	@staticmethod
	def mergeDictionary(x, y):
		"""Merge two dictionary."""
		z = x.copy()
		z.update(y)
		return z
	
	@staticmethod
	def getNextConfigOption(generator):
		'''Finds the next config option tag'''
		notFound = True
		while(notFound):
			try:
				currentToken = next(generator)
					
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
						
					#TODO in case of parse error, remove plugin from list and send a meaningful error message
					return yaml.safe_load(configOptionString)
				
				elif(currentTokenSpelling.startswith("/*")):
					tagIndex = currentTokenSpelling.find(S2ECodeParser.CONFIG_TAG)
					
					if(tagIndex != -1):
						yamlComment = currentTokenSpelling[tagIndex + len(S2ECodeParser.CONFIG_TAG) :-2].replace("\t", "")
						#TODO in case of parse error, remove plugin from list and send a meaningful error message
						return yaml.safe_load(yamlComment)
						
						
			except StopIteration:
				return None
	
	@staticmethod
	def getArgumentList(tokenList, separator = ",", remove = '"'):
		outputList = []
		accumulator = ""
		for token in tokenList:
			if(token.spelling == separator):
				outputList.append(accumulator.replace(remove, ""))
				accumulator = ""
			else:
				accumulator = accumulator + token.spelling
		return outputList
		
			
	@staticmethod
	def printToken(tokenList):
		for token in tokenList:
			print(token.spelling, end='')	
		print("\n")
		
	@staticmethod
	def tokenListToString(tokenList):
		outputString = ""
		for token in tokenList:
			outputString = outputString + token.spelling
		return outputString
		
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
# 	def iterateToken(cursor):
# 		
# 		#Detect the list of following string
# 		#toFind = ["s2e", "(", ")", "->", "getConfig", "(", ")", "->", None, "("]
# 		#toFindPos8 = ["getInt", "getBool"]
# 		toFind = ["S2E_DEFINE_PLUGIN"]
# 		toFindPos = 0
# 		currentToken = ""
# 		generator = cursor.get_tokens()
# 		hasNext = True
# 		
# 		while(hasNext):
# 			try:
# 				currentToken = next(generator)
# 					
# 				# if we found the next element in the list or if it is the item in the 8th positions
# 				if((currentToken.spelling == toFind[toFindPos]) or (toFindPos == 8 and currentToken.spelling in toFindPos8)):
# 					toFindPos = toFindPos + 1
# 					if(toFindPos == len(toFind)):	
# 						toFindPos = 0
# 						print(next(generator).spelling)
# 						print(next(generator).spelling)
# 						print(next(generator).spelling)
# 						print(next(generator).spelling)
# 						print(next(generator).spelling)
# 						#S2ECodeParser.printToken(S2ECodeParser.getUpToCloseParenthesis(generator))
# 				else:
# 					toFindPos = 0
# 					
# 			except StopIteration:
# 				hasNext = False
	
# 	@staticmethod
# 	def iterateChildren(cursor, level = 0):
# 		for c in cursor.get_children():
# 			#if(check == False or c.spelling == head):				
# 			if(c.location.line == 26):
# 				print(S2ECodeParser.levelToString(level) + "display : " + c.displayname)
# 				print(S2ECodeParser.levelToString(level) + "kind : " + str(c.kind))
# 				print(S2ECodeParser.levelToString(level) + "location : " + str(c.location))
# 				print(S2ECodeParser.levelToString(level) + "spelling : " + str(c.spelling))
# 				print(S2ECodeParser.levelToString(level) + "display : " + c.displayname)
# 				print("\n")
# 				
# 			S2ECodeParser.iterateChildren(c, level + 1)
	
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
		


