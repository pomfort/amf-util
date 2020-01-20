from src.util import logger
from lxml import etree
from src.util.xml import strip_ns_prefix
import click
import os
import re

class Transforms:
	"""class for representing a list of transforms in the ACES repository

	member variables:
	root_path -- root path for files
	ctls -- list of CTL objects
	"""

	def __init__(self, root_path):
		"""init empty list"""
		self.root_path = root_path
		self.ctls = list()

	def relative_path_for_transform_id(self, transform_id):
		for ctl in self.ctls:
			if ctl.transform_id == transform_id:
				return ctl.relative_path
		return None

	def transform_id_for_relative_path(self, relative_path):
		for ctl in self.ctls:
			if ctl.relative_path == relative_path:
		         return re.sub(r'^urn:ampas:aces:transformId:v[0-9].[0-9]:', '', ctl.short_transform_id)
		return None

	def description_for_relative_path(self, relative_path):
		for ctl in self.ctls:
			if ctl.relative_path == relative_path:
		         return ctl.description
		return None


class CTL:
	"""class for representing one CTL file
	
	member variables:
	relative_path --
	transform_id --
	"""

	def __init__(self):
		"""init empty list"""
		self.relative_path  = None
		self.transform_id = None
		self.description = None
		self.short_transform_id = None


class TransformsTraverser:
	"""class to read an folder structure of CTL files

	member variables:
	transforms -- Transforms object holding info about all CTLs
	"""

	def __init__(self, root_path):
		self.root_path = root_path
		self.transforms = Transforms(root_path)
		self.traverse()

	def traverse(self):
		"""traversing the folder structure"""
		ctx = click.get_current_context().obj
		if ctx.verbose:
			logger.info(f'traversing \"{self.root_path}\"...')

		for root, directories, filenames in os.walk(self.root_path, topdown=True):
			for filename in sorted(filenames):
				filepath = os.path.join(root, filename)
				if (filepath.endswith(".ctl")):
					ctl = CTL()
					ctl_file = open(filepath, 'r')
					ctl_string = ctl_file.read()
					transform_id = self.extract_tag(ctl_string, "ACEStransformID")

					if transform_id is not None:
						ctl.transform_id = transform_id
						ctl.short_transform_id = re.sub(r'^urn:ampas:aces:transformId:v[0-9].[0-9]:', '', ctl.transform_id)

						ctl.description = self.extract_tag(ctl_string, "ACESuserName")

						relative_path = os.path.relpath(filepath,
													start=self.root_path)
						ctl.relative_path = relative_path

						spec_prefixes = ("ODT", "IDT", "RRT", "LMT", "RRTODT", "ACEScsc",
									"InvODT", "InvIDT", "InvRRT", "InvLMT", "InvRRTODT")
						#spec_prefixes = ("ODT", "IDT", "RRT", "LMT", "RRTODT", "ACEScsc")

						if not ctl.short_transform_id.startswith(spec_prefixes):
							ignore_prefixes = ("ACESlib", "ACESutil", "utilities")
							if not ctl.short_transform_id.startswith(ignore_prefixes):
								logger.error("SKIPPING: wrong prefix \"{0}\"in {1}".format(ctl.short_transform_id, filepath))
						else:
							self.transforms.ctls.append(ctl)
					else:
						logger.error("ERROR: no <ACEStransformID> found in {0}".format(filepath))

	def extract_tag(self, ctl_string, tag_name):
		result = None
		if tag_name is "ACEStransformID":
			found_string = re.search(r'<ACEStransformID>.*<\/ACEStransformID>', ctl_string)
		elif tag_name is "ACESuserName":
			found_string = re.search(r'<ACESuserName>.*<\/ACESuserName>', ctl_string)

		if found_string is not None:
			value = found_string.group(0)
			#value = value[17:]  # remove <ACEStransformID> at start
			#value = value[:-18]  # remove </ACEStransformID> at end
			value = value[(len(tag_name)+2):]
			value = value[:(-(len(tag_name)+3))]
			result = value

		return result

	def log_ctls(self):
		for ctl in self.transforms.ctls:
			logger.info("  found {0}: {1}".format(ctl.short_transform_id, ctl.relative_path))

	def log_ctl_mappings(self):
		for ctl in self.transforms.ctls:
			logger.info("{0}: {1} ({2})".format(ctl.relative_path, ctl.short_transform_id, ctl.description))
