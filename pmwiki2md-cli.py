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

parser.add_argument("-i", "--ignore-codec-read-errors",\
	help="Ignores codec errors when reading source files. This might produce unusable results, however.",\
	action="store_true")

parser.add_argument("--source-encoding",\
	help="Text encoding for source files. Consult python documentation for available encodings and their codes.")

parser.add_argument("--target-encoding",\
	help="Text encoding for target files. Consult python documentation for available encodings and their codes.")

args = parser.parse_args()

converter = FileConverter(conversions=Conversions, filePairs=FilePairs(\
	directoryPaths=FilePairs.DIRECTORY_PATHS(args.source, args.target),\
	suffixes=FilePairs.SUFFIXES(args.source_suffix, args.target_suffix),\
	ignoreCodecReadErrors=args.ignore_codec_read_errors,\
	sourceEncoding=args.source_encoding,\
	targetEncoding=args.target_encoding))
converter.convert()
