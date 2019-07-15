#=======================================================================================
# Imports
#=======================================================================================

# Python
import unittest

# Local

# DEBUG
from lib.debugging import dprint, cdprint
import time, os

#=======================================================================================
# Tests
#=======================================================================================

class IncompleteConversionPair(Exception): pass

class TestFilePair(object):
	
	def __init__(self, pmwikiFilePath, mdFilePath):
		self.pmwikiFilePath = pmwikiFilePath
		self.mdFilePath = mdFilePath
		self._pmwiki = None
		self._md = None
		
	@property
	def pmwiki(self):
		if self._pmwiki is None:
			with open(self.pmwikiFilePath, "r") as pmwikiFile:
				self._pmwiki = pmwikiFile.read()
		return self._pmwiki
	
	@property
	def md(self):
		if self._md is None:
			with open(self.mdFilePath, "r") as mdFile:
				self._md = mdFile.read()
		return self._md
	
	@property
	def convert(self):
		from pmwiki2md import Conversions
		
class FileConversions(unittest.TestCase):
	
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.maxDiff = None
	
	@property
	def conversionsBaseDir(self):
		#return os.listdir(os.path.dirname(__file__))
		return os.path.join(os.path.dirname(__file__), "conversionFiles")
	
	@property
	def pmwikiConversionsBaseDir(self):
		return os.path.join(self.conversionsBaseDir, "pmwiki")
	
	@property
	def mdConversionsBaseDir(self):
		return os.path.join(self.conversionsBaseDir, "md")
		
	@property
	def pmwikiConversionFileNames(self):
		return os.listdir(self.pmwikiConversionsBaseDir)
		
	@property
	def pmwikiConversionFilePaths(self):
		return [os.path.join(self.pmwikiConversionsBaseDir, pmwikiConversionFileName)\
			for pmwikiConversionFileName in self.pmwikiConversionFileNames]
		
	def getConversionNameFromConversionFileName(self, conversionFileName):
		return conversionFileName.rpartition(".")[0]
	
	def getMdFileNameFromPmwikiFileName(self, pmwikiFileName):
		return self.getConversionNameFromConversionFileName(pmwikiFileName)+".md"
		
	def getMatchingMdFilePathForPmwikiFilePath(self, pmwikiFilePath):
		pmwikiFileName = os.path.basename(pmwikiFilePath)
		mdFilePath = os.path.join(self.mdConversionsBaseDir, self.getMdFileNameFromPmwikiFileName(pmwikiFileName))
		if os.path.exists(mdFilePath):
			return mdFilePath
		else:
			raise IncompleteConversionPair("Markdown counterpart for pmwiki file not found: "+pmwikiFilePath)
		
	def setUp(self):
		self.filePairs = {}
		for pmwikiFilePath in self.pmwikiConversionFilePaths:
			pmwikiFileName = pmwikiFilePath.rpartition(os.sep)[2]
			pmwikiFileTestName, pmwikiFileNameSuffix = pmwikiFileName.rpartition(".")[0::2]
			if pmwikiFileNameSuffix == "pmwiki":
				self.filePairs[pmwikiFileTestName] = (TestFilePair(\
					pmwikiFilePath,\
					self.getMatchingMdFilePathForPmwikiFilePath(pmwikiFilePath)))
				
	def _runOneFileTest(self, filePair):
		from pmwiki2md import AllConversions as Conversions, Content as Content
		conversions = Conversions()
		pmwikiFilePath = os.path.join(self.pmwikiConversionsBaseDir, "testTest.pmwiki")
		mdFilePath = self.getMatchingMdFilePathForPmwikiFilePath(pmwikiFilePath)
		testFilePair = TestFilePair(pmwikiFilePath, mdFilePath)
		dprint("testFilePair", testFilePair.pmwikiFilePath, testFilePair.mdFilePath)
		self.assertEqual(conversions.convert(Content(testFilePair.pmwiki)).string, testFilePair.md)
		
	def runOneFileTest(self, pmwikiFileTestName):
		from pmwiki2md import AllConversions as Conversions, Content as Content
		conversions = Conversions()
		testFilePair = self.filePairs[pmwikiFileTestName]
		self.assertEqual(conversions.convert(Content(testFilePair.pmwiki)).string, testFilePair.md)
		
	def test_test(self):
		self.runOneFileTest("testTest")
		
	def test_twoElements(self):
		self.runOneFileTest("twoElements")
		
	def test_twoElementsWithLinebreak(self):
		self.runOneFileTest("twoElementsWithLinebreak")
		
	def test_hallowelt(self):
		self.runOneFileTest("hallowelt")
