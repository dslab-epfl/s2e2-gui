from __future__ import unicode_literals
from __future__ import print_function

import clang.cindex
import os
import sys

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
	
	LIST_TYPE = "list"
	BOOLEAN_TYPE = "bool"
	INT_TYPE = "int"
	STRING_TYPE = "string"
	STRING_LIST_TYPE = "stringList"
	INT_LIST_TYPE = "intList"
	ACCEPTED_TYPES = [BOOLEAN_TYPE, INT_TYPE, STRING_TYPE, STRING_LIST_TYPE, INT_LIST_TYPE, LIST_TYPE]
	
	TYPE_KEY = "type"
	DESCRIPTION_KEY = "description"
	CONTENT_KEY = "content"
	
	
	@staticmethod
	def parsePluginsInDir(dirPath, pluginNameList):
		everyPluginDict = []
		for root, dirs, files in os.walk(dirPath):
			for file in files:
				if(file in pluginNameList):
					try:
						pluginDict = S2ECodeParser.parsePlugin(os.path.abspath(os.path.join(root, file)))
						everyPluginDict.append(pluginDict)
					except PluginParseException as err:
						print("\033[0;31;49m " + str(err.value) + "\033[0m")
					
		with open("result.json", "w") as fp:
			json.dump(everyPluginDict, fp, indent=4, separators=(',', ': '))
		
	
	@staticmethod
	def parsePlugin(filePath):
		index = clang.cindex.Index.create()
		tu = index.parse(filePath)
		print('Parsing File :', tu.spelling)
		
		pluginName, pluginDescr, pluginDep = S2ECodeParser.getPluginInfo(tu.cursor)
		
		try:
			configDictionary = S2ECodeParser.getAllConfigOption(tu.cursor)
		except yaml.scanner.ScannerError as err:
			raise PluginParseException(str(err))
		
		S2ECodeParser.checkAndCleanConfigDictionary(configDictionary)
		
		pluginDictionary = {}
		pluginDictionary["name"] = pluginName
		pluginDictionary["description"] = pluginDescr
		pluginDictionary["dependencies"] = pluginDep
		pluginDictionary["configOption"] = configDictionary

		return pluginDictionary
	
			
	@staticmethod
	def checkAndCleanConfigDictionary(dict):
		for key, value in dict.iteritems():
			if(not(S2ECodeParser.TYPE_KEY in value)):
				raise PluginParseException(str(key) + "has no type")
			if(not(value[S2ECodeParser.TYPE_KEY] in S2ECodeParser.ACCEPTED_TYPES)):
				raise PluginParseException(str(key) + " as an illegal type of " + str(value[S2ECodeParser.TYPE_KEY]))
			if(not (S2ECodeParser.DESCRIPTION_KEY in value)):
				value[S2ECodeParser.DESCRIPTION_KEY]=""
				
			
			# Need to deal with list dict in a different way
			keyType = value[S2ECodeParser.TYPE_KEY]
			if(keyType == S2ECodeParser.LIST_TYPE):
				# Check if the list as a content
				if(not (S2ECodeParser.CONTENT_KEY in value)):
					raise PluginParseException(str(key) + " is a list without a content attribute. List must have a content ")
				
				for valueKey in value.keys():
					if(valueKey!= S2ECodeParser.CONTENT_KEY and valueKey != S2ECodeParser.TYPE_KEY and valueKey != S2ECodeParser.DESCRIPTION_KEY):
						value.pop(valueKey)
				S2ECodeParser.checkAndCleanConfigDictionary(value[S2ECodeParser.CONTENT_KEY])
			else:
				for valueKey in value.keys():
					if(valueKey != S2ECodeParser.TYPE_KEY and valueKey != S2ECodeParser.DESCRIPTION_KEY):
						value.pop(valueKey)
			
			
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
	def isComment(string):
		if(string.startswith("//") or string.startswith("/*")):
			return True;
		else:
			return False;
	
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
		'''Merge two dictionary.'''
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
						
					return yaml.safe_load(configOptionString)
				
				elif(currentTokenSpelling.startswith("/*")):
					tagIndex = currentTokenSpelling.find(S2ECodeParser.CONFIG_TAG)
					
					if(tagIndex != -1):
						yamlComment = currentTokenSpelling[tagIndex + len(S2ECodeParser.CONFIG_TAG) :-2].replace("\t", "")
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
		if(len(accumulator) > 0):
			outputList.append(accumulator.replace(remove, ""))
		
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
        