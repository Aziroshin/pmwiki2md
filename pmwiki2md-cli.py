#!/usr/bin/env python3
#-*- coding: utf-8 -*-

# Python
import argparse

# Local
from lib import converter
from lib.converter import FileConverter, FilePairs
from lib.pmwiki2md import AllConversions as Conversions

DEFAULT_SOURCE_SUFFIX = "pmwiki"
DEFAULT_TARGET_SUFFIX = "md"

parser = argparse.ArgumentParser()
parser.add_argument("source", help="Directory of files to be converted.")
parser.add_argument("target", help="Directory to write converted files to.")

parser.add_argument("--source-suffix",\
	help="Only source files with that suffix will be considered for conversion. Default:"
	"{default}".format(default=DEFAULT_SOURCE_SUFFIX),\
	default=DEFAULT_SOURCE_SUFFIX)

parser.add_argument("--target-suffix",\
	help="Suffix to add to converted files. Default:"
	"{default}".format(default=DEFAULT_TARGET_SUFFIX),\
	default=DEFAULT_TARGET_SUFFIX)
args = parser.parse_args()

converter = FileConverter(conversions=Conversions, filePairs=FilePairs(\
	directoryPaths=FilePairs.DIRECTORY_PATHS(\
		source=args.source,\
		target=args.target),\
	suffixes=FilePairs.SUFFIXES(\
		source=args.source_suffix,\
		target=args.target_suffix)))
converter.convert()
