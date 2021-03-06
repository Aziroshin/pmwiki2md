#-*- coding: utf-8 -*-

#=======================================================================================
# Imports
#=======================================================================================

# Python
from pathlib import Path
from collections import UserList
from typing import NamedTuple
from lib.pmwiki2md import Content

# Local
from lib.datatypes import NamedList

# Debugging
import sys

#=======================================================================================
# Library
#=======================================================================================

class File(object):
	
	"""Text file handler with content cache.
	
	Assumes it's the only thing in the world that accesses
	the file in question concurrently.
	
	Takes:
		path (Path)
	Has:
		- path (Path)
			pathlib.Path object from specified path.
		- _cachedContent (None || str)
			Contains file's contents. Starts with None, and gets
			set to None every time .write() is called.
			Is initialized with the file's content every time
			.content is called AND this is found to be None."""
	
	def __init__(self, pathObj, ignoreCodecReadErrors=False, encoding=None):
		self.path = pathObj
		self.ignoreCodecReadErrors = ignoreCodecReadErrors
		self._encoding = encoding
		self._cachedContent = None
		
	@property
	def exists(self):
		return self.path.exists()
		
	@property
	def isDirectory(self):
		return self.path.is_dir()
	
	@property
	def parentDir(self):
		return self.path.parent
	
	@property
	def name(self):
		return self.path.name
	
	@property
	def nameWithoutSuffix(self):
		return self.path.stem
	
	@property
	def encoding(self):
		"""Which encoding to use for our operations."""
		if self._encoding:
			return self._encoding
		else:
			return None
	
	@property
	def content(self):
		
		"""File's cached content.
		Initializes cache if it's empty."""
		
		if self._cachedContent == None:
			self._cachedContent = self.read()
		return self._cachedContent
	
	def read(self):
		
		# Configure handling of encoding related errors while reading.
		if self.ignoreCodecReadErrors:
			errorHandler="ignore"
		else:
			errorHandler = None
		
		# Read.
		with open(str(self.path), "r", errors=errorHandler, encoding=self.encoding) as fileObj:
			return fileObj.read()
		
	def write(self, content):
		
		"""Write specified content and reset content cache."""
		
		with open(str(self.path), "w", encoding=self.encoding) as fileObj:
			self._cachedContent = None
			return fileObj.write(content)
		
class FilePair(object):
	
	def __init__(self, sourcePathObj, targetPathObj, ignoreCodecReadErrors=False,\
		sourceEncoding=None, targetEncoding=None):
		self.source = File(sourcePathObj, ignoreCodecReadErrors=ignoreCodecReadErrors,\
			encoding=sourceEncoding)
		self.target = File(targetPathObj, ignoreCodecReadErrors=ignoreCodecReadErrors,\
			encoding=targetEncoding)
		
class FilePairs(UserList):
	
	"""Initializes pairs either from list of FilePair objects or directories.
	
	Takes:
		- pairs ([FilePair]), default: []
		- directoryPaths (None || self.__class__.DIRECTORY_PATHS), default: None
			Tuple with a source and a target directory to initialize
			file pairs from.
		- suffixes (None || self.__class__.SUFFIXES), default: None
			Tuple with a suffix for source and one for target files.
			If non-empty, source will serve as a filter to choose only
			files from the source directory with that suffix.
			If non-empty, target will serve as a suffix to add to all
			target files."""
			
	class DIRECTORY_PATHS(NamedList):
		"""Source and target paths as strings."""
		ATTRIBUTES = ["source", "target"]
		
	class DIRECTORIES(NamedList):
		"""Source and target paths as pathlib.PATH objects."""
		ATTRIBUTES = ["source", "target"]
		
	class SUFFIXES(NamedList):
		"""Source and target file name suffixes as strings."""
		ATTRIBUTES = ["source", "target"]
		
	def __init__(self, pairs=[], directoryPaths=None, suffixes=None, ignoreCodecReadErrors=False,\
		sourceEncoding=None, targetEncoding=None):
		self.data = []
		self.ignoreCodecReadErrors = ignoreCodecReadErrors
		self.sourceEncoding = sourceEncoding
		self.targetEncoding = targetEncoding
		if not suffixes == None:
			self.suffixes = suffixes
		else:
			self.suffixes = None
		if not directoryPaths == None:
			self.directories = self.__class__.DIRECTORIES(\
				source=Path(directoryPaths.source),\
				target=Path(directoryPaths.target))
			self.data = self.data + self.fromDirs(self.directories, self.suffixes)
		else:
			self.directories = None
		
	@property
	def iFilterForSuffix(self):
		
		"""Filter source dirs to include files with a specific suffix only?"""
		
		if self.suffixes:
			if self.suffixes.source:
				return True
		return False
	
	@property
	def iAppendSuffix(self):
		
		"""Append suffix to target file paths?"""
		
		if self.suffixes:
			if self.suffixes.target:
				return True
		return False
		
	def dottedSuffix(self, suffix):
		"""Always return the input with a dot prefixed.
		If it already has one, nothing changes."""
		if len(suffix) > 0:
			if not suffix.startswith("."):
				return "."+suffix
		return suffix
		
	def fromDirs(self, directories, suffixes):
		
		"""Walk source directory and initialize file pairs.
		Every eligible file in the source directory will get a file pair,
		whereas the target file of the pair will be assembled from the
		source file name, a suffix if configured so and the target dir path.
		Which file counts as eligible can be determined by specifying
		a source file suffix.
		
		Returns a FilePairs object (which is a collections.UserList subclass)."""
		
		filePairs = []
		for filePath in directories.source.iterdir():
			
			if self.iFilterForSuffix:
				if not filePath.suffix == self.dottedSuffix(suffixes.source):
					# Seems like we're picky as to which file to take. Next!
					continue
				
			sourcePath = filePath
			
			# Assemble target file name.
			targetFileName = sourcePath.stem
			if self.iAppendSuffix:
				targetFileName = targetFileName+self.dottedSuffix(suffixes.target)
			
			targetPath = Path(directories.target, targetFileName)
			filePairs.append(FilePair(sourcePath, targetPath, ignoreCodecReadErrors=self.ignoreCodecReadErrors,\
				sourceEncoding=self.sourceEncoding, targetEncoding=self.targetEncoding))
		
		return filePairs
	
class FileConverter(object):
	
	"""Converts files using a collection of conversions.
	Takes:
		conversions (Conversions)
			Conversions object configured with the Conversion classes to be used.
		filePairs ([FilePair])
			List of FilePair objects configured with the file paths to be used.
			"""
	
	def __init__(self, conversions, filePairs=[]):
		self.conversions = conversions
		self.filePairs = filePairs
		
	def convert(self):
		for pair in self.filePairs:
			converted = self.conversions().convert(Content(pair.source.read()))
			pair.target.write(converted.string)
