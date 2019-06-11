#=======================================================================================
# Imports
#=======================================================================================

# Python
import unittest

# Local

# DEBUG
from lib.debugging import dprint, cdprint
import time

#=======================================================================================
# Tests
#=======================================================================================

class TestFilePair(object):
	
	def __init__(self, pmwikiFilePath, mdFilePath):
		self.pmwikiFilePath = pmwikiFilePath
		self.mdFilePath = pmwikiFilePath
		
		
	@property
	def pmwiki(self):
		if self._pmwiki is None:
			with open(self.pmwikiFilePath, "r") as pmwikiFile:
				self._pmwiki = pmwikiFile.read().encode()
		return self._pmwiki
	
	@property
	def md(self):
		if self._md is None:
			with open(self.mdFilePath, "r") as mdFile:
				self._md = mdFile.read().encode()
		return self._md
	
	@property
	def isIdentical(self):
		return self.pmwiki == self.md
	
class FileConversions(unittest.TestCase):
	
	@property
	def conversionsBaseDir(self):
		return os.listdir(os.path.dirname(__file__)
	
	@property
	def pmwikiConversionsBaseDir(self):
		return os.path.join(self.conversionsBaseDir, "pmwiki")
		
	def setUp(self):
		for pmwikiFile in :
			os.path.join(os.path.dirname(__file__ pmwikiFile)
