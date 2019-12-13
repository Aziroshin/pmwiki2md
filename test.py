#!/usr/bin/env python3
#-*- coding: utf-8 -*-

"""Runs testing modules from the testing directory. Not to confuse with unit tests."""
# Convention: "tests" like these will be called "testings" throughout the codebase.
# "testings" are everything test related that doesn't fit the unit test paradigm,
# typically geared towards analyzing what's appening in the application for development
# and debugging purposes.

#=======================================================================================
# Imports
#=======================================================================================
#==========================================================
#=============================

import unittest
from pathlib import Path
import argparse
import os
import sys
from collections import UserDict, UserList

# Debug
from lib.debugging import dprint

#=======================================================================================
# Configuration
#=======================================================================================

TESTS_DIR = str(Path(Path(__file__).absolute().parent, "tests"))
IGNORED_DIRS = ["data", "lib", "__pycache__"]

#=======================================================================================
# Library
#=======================================================================================

#=============================
# Arguments
#=============================

class Arguments(object):
	
	#=============================
	"""A basic class for the setup for the arguments we take. Override .setUp() to implement."""
	#=============================
	
	def __init__(self):
		self.parser = argparse.ArgumentParser()
		self.setUp()
		
	def setUp(self):
		"""Override this with your particular argument configuration."""
		pass
	
	def get(self):
		"""Get the initialized argparse.Namespace object for our arguments."""
		return self.parser.parse_args()

#=============================
# Testing
#=============================

class TestDirModuleList(UserList):
	
	def __init__(self, dirPath):
		self.data = []
		for fileName in os.listdir(str(Path(dirPath))):
			if self.isTestModule(Path(dirPath, fileName)):
				self.append(Path(fileName).stem)
		
	def isTestModule(self, path):
		"""Returns True if path seems to point to a python test module, False otherwise."""
		#if not path.name == "__init__.py":
		if path.suffix == ".py" and not path.stem == "__init__":
			return True
		else:
			return False

class Tests(UserDict):
	
	def __init__(self, path, types=None, modules=None):
		self.path = path
		self.specifiedTypes = types
		self.specifiedModules = modules
		self.data = self.get(types, modules)
	
	@property
	def allTypes(self):
		"""List of all test types as found in the specified tests directory."""
		types = []
		for fileName in os.listdir(self.path):
			filePath = Path(self.path, fileName)
			if filePath.is_dir() and filePath.name not in IGNORED_DIRS:
				types.append(fileName)
		return types
	
	def get(self, types, modules):
		"""Get a set of tests as specified.
		If types got specified, will only consider tests from those directories.
		If modules got specified, will only consider test modules with the specified
		module names from the considered type directories."""
		tests = {}
		if types is None:
			types = self.allTypes
		for testType in types:
			tests[testType] = []
			for test in TestDirModuleList(Path(self.path, testType)):
				if self.specifiedModules is not None:
					if test not in self.specifiedModules:
						continue
				tests[testType].append(test)
		return tests

	@property
	def types(self):
		return list(self.keys())
	
	@property
	def modules(self):
		return list(self.values())

class TestParameterValues(UserList):
	def __init__(self, specifiedValues):
		
		self.specifiedValues = specifiedValues
		
		# Cache a list of all test types and test modules and initialize our list.
		self.tests = Tests(TESTS_DIR)
		self.data = [self.defaultTypes, self.defaultModules]

		# Fill in the test types and modules as they were specified by the user.
		if not specifiedValues is None:
			if self.typesGotSpecified:
				self.types = self.specifiedTypes
				if self.modulesGotSpecified:
					self.modules = self.specifiedModules
	
	#=============================
	# Determinators as to the anatomy of the values specified.

	# Types.
	@property
	def typesGotSpecified(self):
		"""Has the user specified test types?"""
		return len(self.specifiedValues) > 0
	@property
	def specifiedTypes(self):
		"""List of test types as specified by the user."""
		return self.specifiedValues[0]
	
	# Modules.
	@property
	def modulesGotSpecified(self):
		"""Has the user specified test modules?"""
		return len(self.specifiedValues) > 1
	@property
	def specifiedModules(self):
		"""List of test modules as specified by the user."""
		return self.specifiedValues[1]
	
	#=============================
	# Defaults.
	
	@property
	def defaultTypes(self):
		"""Test types we're going to use if none are specified."""
		return self.tests.types
	
	@property
	def defaultModules(self):
		"""Test modules we're going to run if none are specified."""
		return self.tests.modules
	
	#=============================
	# Handling of the types list.
	
	@property
	def types(self):
		"""Test types as configured."""
		return self[0]
	
	@types.setter
	def types(self, types):
		self[0] = types
	
	#=============================
	# Handling of the modules list.
	
	@property
	def modules(self):
		"""Test modules as configured."""
		return self[1]
	
	@modules.setter
	def modules(self, modules):
		self[1] = modules

class TestingArguments(Arguments):
	
	#=============================
	"""A basic class for the setup for the arguments we take. Override .setUp() to implement."""
	#=============================
	
	def setUp(self):
		
		""" We take a single argument besides argparse's defaults: Name of the testing module to load.
		Upon calling --help, we'll also list all the available modules from the testing directory."""
		
		self.parser.add_argument("-a", "--all", action="store_false",help="Run all tests")
		self.parser.add_argument("tests", nargs='*', default=None, help=\
			"There are two parameters, the first being the type of test, the second the"
			"name of the test."
			"Test types: {unit, integration}"
			"Example: test.py integration processing")

def runModule(testType, module):
	chosenModule = __import__(name="tests.{testType}.{moduleName}"\
		.format(moduleName=module, testType=testType),\
			globals=globals(), locals=locals(), fromlist=[module], level=0)
	#chosenModule.Testing().run()
	suite = unittest.defaultTestLoader.loadTestsFromModule(chosenModule)
	unittest.TextTestRunner(verbosity=2).run(suite)

def runModules(types, modules):
	# NOTE: As a result of design flaws in some of the code in this module,
	# we have to iterate through lists in 'modules'. A much better approach
	# would be to make the 'Tests' class alterable, design it with
	# filters and work with that here.
	dprint("types:", types, "modules", modules)
	testTypeIndex = 0
	for testType in types:
		for module in modules[testTypeIndex]:
			runModule(testType, module)
		testTypeIndex += 1

#=======================================================================================
# Action
#=======================================================================================

if __name__ == "__main__":
	
	args = TestingArguments().get()
	tests = Tests(TESTS_DIR)
	from lib import pmwiki2md
	if len(args.tests) == 0:
		for testType in tests:
			for module in tests[testType]:
				runModule(testType, module)
	else:
		if len(args.tests) == 2:
			runModule(args.tests[0], args.tests[1])
		else:
			for module in tests[args.tests[0]]:
				runModule(args.tests[0], module)
