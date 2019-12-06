from src.util import logger
from lxml import etree
from src.util.xml import strip_ns_prefix
import click
import os
import re

amfutil_toolname_string = 'amf-util'
amfutil_toolversion_string = '0.0.1'


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
					result = re.search(r'<ACEStransformID>.*<\/ACEStransformID>', ctl_string)
					if result is not None:
						transform_id = result.group(0)
					else:
						logger.error("no <ACEStransformID> found in {0}".format(filepath))

					ctl.transform_id = transform_id.lstrip("<ACEStransformID>").rstrip("</ACEStransformID>")
					relative_path = os.path.relpath(filepath,
													start=self.root_path)
					ctl.relative_path = relative_path
					self.transforms.ctls.append(ctl)

	def log_ctls(self):
		for ctl in self.transforms.ctls:
			logger.info("  found {0}: {1}".format(ctl.transform_id, ctl.relative_path))
