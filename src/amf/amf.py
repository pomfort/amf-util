from src.util import logger
from src.ctl import ctl
from lxml import etree
from src.util.xml import strip_ns_prefix
import click
import os

amfutil_toolname_string = 'amf-util'
amfutil_toolversion_string = '0.0.1'


class AcesMetadataFile:
    """class for representing a list of media hashes, e.g. from an MHL file,
    also uses MediaHash and HashEntry class for storing information

    member variables:
    root_path -- root path for files
    info -- contents of <amfInfo>
    pipeline -- contents of <pipeline>
    """

    def __init__(self, root_path):
        """init empty list"""
        self.root_path = root_path
        self.info = Info()
        self.pipeline = Pipeline()


class Info:
    """class for representing contents of the amfInfo tag

    member variables:
    description --
    uuid --
    dateTime --
    """

    def __init__(self):
        """init empty list"""
        self.description = None
        self.uuid = None
        self.creation_date_time = None
        self.modification_date_time = None


class Pipeline:
    """class for representing contents of the amf:pipeline tag

    member variables:
    """

    def __init__(self):
        """init empty list"""
        self.info = None
        self.input_transforms = list()
        self.look_transforms = list()
        self.output_transforms = list()

class Transform:
    """class for holding information of one transform

    member variables:
    """

    def __init__(self):
        """init empty list"""
        self.type = None
        self.description = None
        self.transform_id = None


class AmfFileReader:
    """class to read an AMF file into a AcesMetadataFile object

    member variables:
    filepath -- path to AMF file
    aces_metadata_file -- AcesMetadataFile object representing the AMF file
    """

    def __init__(self, filepath):
        self.filepath = filepath
        self.aces_metadata_file = None
        self.parse()

    def parse(self):
        """parsing the AMF XML file and building the AcesMetadataFile for the aces_metadata_file member variable"""
        ctx = click.get_current_context().obj
        if ctx.verbose:
            logger.info(f'parsing \"{os.path.basename(self.filepath)}\"...')

        tree = etree.parse(self.filepath)
        tree = strip_ns_prefix(tree)				# otherwise we need to specify fully prefix'ed element names

        acesmetadatafile_element = tree.getroot()

        self.aces_metadata_file = AcesMetadataFile(None)

        for section_element in acesmetadatafile_element.getchildren():
            if section_element.tag == 'amfInfo':
                if ctx.verbose:
                    logger.info(f'  extracting <amfInfo>...')
                for info_element in section_element.getchildren():
                    if info_element.tag == 'description':
                        self.aces_metadata_file.info.description = info_element.text
                    if info_element.tag == 'uuid':
                        self.aces_metadata_file.info.uuid = info_element.text
                    if info_element.tag == 'dateTime':
                        if ctx.verbose:
                            logger.info(f'    extracting <dateTime>...')
                        for date_element in info_element.getchildren():
                            if date_element.tag == 'creationDateTime':
                                self.aces_metadata_file.info.creation_date_time = date_element.text
                            if date_element.tag == 'modificationDateTime':
                                self.aces_metadata_file.info.modification_date_time = date_element.text
            if section_element.tag == 'pipeline':
                if ctx.verbose:
                    logger.info(f'  extracting <pipeline>...')
                for pipeline_element in section_element.getchildren():
                    if pipeline_element.tag == 'inputTransform':
                        if ctx.verbose:
                            logger.info(f'    extracting <inputTransform>...')
                        # TODO: implement
                    if pipeline_element.tag == 'lookTransform':
                        if ctx.verbose:
                            logger.info(f'    extracting <lookTransform>...')
                        # TODO: implement
                    if pipeline_element.tag == 'outputTransform':
                        if ctx.verbose:
                            logger.info(f'    extracting <outputTransform>...')
                        for output_element in pipeline_element.getchildren():
                            transform = Transform()
                            if output_element.tag == 'referenceRenderingTransform':
                                transform.type = 'RRT'
                            elif output_element.tag == 'outputDeviceTransform':
                                transform.type = 'ODT'
                            for rrt_element in output_element.getchildren():
                                if rrt_element.tag == 'description':
                                    transform.description = rrt_element.text
                                if rrt_element.tag == 'transformID':
                                    transform.transform_id = rrt_element.text
                            self.aces_metadata_file.pipeline.output_transforms.append(transform)

    def log_info(self):
        ctx = click.get_current_context().obj
        if ctx.compact:
            logger.info("{0}: {1}".format(self.filepath, self.aces_metadata_file.info.uuid))
        else:
            logger.info("{0}:".format(self.filepath))
            logger.info("           description: {0}".format(self.aces_metadata_file.info.description))
            logger.info("                  uuid: {0}".format(self.aces_metadata_file.info.uuid))
            logger.info("      creationDateTime: {0}".format(self.aces_metadata_file.info.creation_date_time))
            logger.info("  modificationDateTime: {0}".format(self.aces_metadata_file.info.modification_date_time))

            for transform in self.aces_metadata_file.pipeline.input_transforms:
                logger.info("                  {0}: {1} ({2})".format(transform.type, transform.transform_id, transform.description))
            for transform in self.aces_metadata_file.pipeline.look_transforms:
                logger.info("                  {0}: {1} ({2})".format(transform.type, transform.transform_id, transform.description))
            for transform in self.aces_metadata_file.pipeline.output_transforms:
                logger.info("                  {0}: {1} ({2})".format(transform.type, transform.transform_id, transform.description))


    def log_render(self, ctl_transforms, ctl_root_path):
        logger.info("# {0}".format(self.filepath))
        logger.info("# created by {0} {1}".format(amfutil_toolname_string, amfutil_toolversion_string))
        logger.info("# transforms:")

        for transform in self.aces_metadata_file.pipeline.input_transforms:
            logger.info("#   {0}: {1} ({2})".format(transform.type, transform.transform_id, transform.description))
        for transform in self.aces_metadata_file.pipeline.look_transforms:
            logger.info("#   {0}: {1} ({2})".format(transform.type, transform.transform_id, transform.description))
        for transform in self.aces_metadata_file.pipeline.output_transforms:
            logger.info("#   {0}: {1} ({2})".format(transform.type, transform.transform_id, transform.description))

        logger.info("\nCTLRENDER=`which ctlrender`\n")
        logger.info("export CTL_MODULE_PATH=\"{0}/utilities/\"\n".format(ctl_root_path))

        logger.info("$CTLRENDER \\")
        for transform in self.aces_metadata_file.pipeline.output_transforms:
            logger.info("    -ctl {0}/{1} \\".format(
                ctl_root_path,
                ctl_transforms.relative_path_for_transform_id(transform.transform_id)))
        logger.info("     -force \\")
        logger.info("     path/to/input-file.tiff \\")
        logger.info("     path/to/output-file.tiff")
