"""
__author__ = "Patrick Renner"
__copyright__ = "Copyright 2020, Pomfort GmbH"

__license__ = "MIT"
__maintainer__ = "Patrick Renner"
__email__ = "opensource@pomfort.com"
"""

from src.util import logger
from lxml import etree
from src.util.xml import strip_ns_prefix
import click
import os
import re

amfutil_toolname_string = 'amf-util'
amfutil_toolversion_string = '0.0.3'

# error codes
amfutil_error_cannot_find_transform = 101


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

    def resolve_relative_paths(self, ctl_transforms):
        for transform in self.input_transforms:
            relative_path = ctl_transforms.relative_path_for_transform_id(transform.short_transform_id())
            if relative_path is None and transform.applied is False:
                logger.error("WARNING: transformId \"{0}\" not found in CTLs".format(transform.short_transform_id()))
                relative_path = "???"
            transform.relative_path = relative_path

        for transform in self.look_transforms:
            relative_path = ctl_transforms.relative_path_for_transform_id(transform.short_transform_id())
            if relative_path is None:
                logger.error("Cannot find a transform for lookTransform {0}!".format(transform.short_transform_id()))
                exit(amfutil_error_cannot_find_transform)
            else:
                transform.relative_path = relative_path

        for transform in self.output_transforms:
            relative_path = ctl_transforms.relative_path_for_transform_id(transform.short_transform_id())
            if relative_path is None:
                logger.error("Cannot find a transform for outputTransform {0}!".format(transform.short_transform_id()))
                exit(amfutil_error_cannot_find_transform)
            else:
                transform.relative_path = relative_path


class Transform:
    """class for holding information of one transform

    member variables:
    """

    def __init__(self):
        """init empty list"""
        self.type = None
        self.description = None
        self.transform_id = None
        self.file = None
        self.applied = False
        self.relative_path = None
        self.hash_string = None

    def short_transform_id(self):
        # TODO: what can the version string be? (e.g. urn:ampas:aces:transformId:v1.5)
        if self.transform_id is not None:
            return re.sub(r'^urn:ampas:aces:transformId:v[0-9].[0-9]:', '', self.transform_id)
        else:
            return self.transform_id


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
                        regularIDT = True
                        if ctx.verbose:
                            logger.info(f'    extracting <inputTransform>...')
                        transform = Transform()
                        if pipeline_element.tag == 'transformId':
                            transform.type = '???'
                            transform.transform_id = pipeline_element.text
                        else:
                            if pipeline_element.tag == 'inputTransform':
                                applied_attribute = pipeline_element.get('applied')
                                if applied_attribute == 'true':
                                    transform.applied = True
                            for idt_element in pipeline_element.getchildren():
                                if idt_element.tag == 'transformId' or idt_element.tag == 'transformID':
                                    transform.transform_id = idt_element.text
                                    transform.type = 'IDT'
                                if idt_element.tag == 'description':
                                    transform.description = idt_element.text
                                # TODO: find out if 'transformId' (introduced in examples in Jan 2020) or 'transformID'
                                if idt_element.tag == 'inverseOutputDeviceTransform':
                                    transform = Transform()
                                    for invodt_element in idt_element.getchildren():
                                        if invodt_element.tag == 'transformId' or invodt_element.tag == 'transformID':
                                            transform.transform_id = invodt_element.text
                                            transform.type = 'InvODT'
                                        if invodt_element.tag == 'description':
                                            transform.description = invodt_element.text
                                    self.aces_metadata_file.pipeline.output_transforms.append(transform)
                                    regularIDT=False
                                if idt_element.tag == 'inverseReferenceRenderingTransform':
                                    transform = Transform()
                                    for invrrt_element in idt_element.getchildren():
                                        if invrrt_element.tag == 'transformId' or invrrt_element.tag == 'transformID':
                                            transform.transform_id = invrrt_element.text
                                            transform.type = 'InvRRT'
                                        if invrrt_element.tag == 'description':
                                            transform.description = invrrt_element.text
                                    self.aces_metadata_file.pipeline.output_transforms.append(transform)
                                    regularIDT = False
                        if regularIDT:
                            self.aces_metadata_file.pipeline.input_transforms.append(transform)

                    if pipeline_element.tag == 'lookTransform':
                        if ctx.verbose:
                            logger.info(f'    extracting <lookTransform>...')

                        transform = None
                        for lmt_element in pipeline_element.getchildren():
                            if lmt_element.tag == 'transformId' or lmt_element.tag == 'description' or \
                                    lmt_element.tag == 'hash' or lmt_element.tag == 'file':
                                # LMT
                                if transform == None:
                                    transform = Transform()
                                    transform.type = 'LMT'
                                if lmt_element.tag == 'transformId':
                                    transform.transform_id = lmt_element.text
                                if lmt_element.tag == 'file':
                                    transform.file = lmt_element.text
                                if lmt_element.tag == 'description':
                                    transform.description = lmt_element.text
                                if lmt_element.tag == 'hash':
                                    transform.hash_string = lmt_element.text
                        if transform is not None and transform.type == 'LMT':
                            self.aces_metadata_file.pipeline.look_transforms.append(transform)

                        # TODO: implement

                    if pipeline_element.tag == 'outputTransform':
                        if ctx.verbose:
                            logger.info(f'    extracting <outputTransform>...')

                        transform = None
                        for output_element in pipeline_element.getchildren():
                            if output_element.tag == 'transformId' or output_element.tag == 'description' or output_element.tag == 'hash' :
                                # HDR: RRTODT
                                if transform == None:
                                    transform = Transform()
                                    transform.type = 'RRTODT'
                                if output_element.tag == 'transformId':
                                    transform.transform_id = output_element.text
                                if output_element.tag == 'description':
                                    transform.description = output_element.text
                                if output_element.tag == 'hash':
                                    transform.hash_string = output_element.text
                            else:
                                # SDR: RRT + ODT
                                transform = Transform()
                                if output_element.tag == 'referenceRenderingTransform':
                                    transform.type = 'RRT'
                                elif output_element.tag == 'outputDeviceTransform':
                                    transform.type = 'ODT'
                                for rrt_element in output_element.getchildren():
                                    if rrt_element.tag == 'description':
                                        transform.description = rrt_element.text
                                    if rrt_element.tag == 'transformId':
                                        transform.transform_id = rrt_element.text
                                self.aces_metadata_file.pipeline.output_transforms.append(transform)

                        if transform.type == 'RRTODT':
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
                self.log_transform_for_info(transform)
            for transform in self.aces_metadata_file.pipeline.look_transforms:
                self.log_transform_for_info(transform)
            for transform in self.aces_metadata_file.pipeline.output_transforms:
                self.log_transform_for_info(transform)

    def log_transform_for_info(self, transform):
        applied_string = ""
        if transform.applied is True:
            applied_string = " [applied=\"true\"]"

        identifier_string = ""
        if transform.transform_id is not None:
            identifier_string = transform.short_transform_id()
            if transform.file is not None:
                identifier_string = identifier_string + "/\"" + transform.file + "\""
        elif transform.file is not None:
            identifier_string = "\"" + transform.file + "\""
        else:
            identifier_string = "?"

        logger.info("                   {0}: {1}{2} ({3})".format(transform.type,
                                                                  identifier_string,
                                                                  applied_string,
                                                                  transform.description))

    def log_render(self, ctl_transforms, ctl_root_path):

        self.aces_metadata_file.pipeline.resolve_relative_paths(ctl_transforms)
        logger.info("#!/bin/bash")
        logger.info("")
        logger.info("# {0}".format(self.filepath))
        logger.info("# created by {0} {1}".format(amfutil_toolname_string, amfutil_toolversion_string))
        logger.info("# transforms:")

        for transform in self.aces_metadata_file.pipeline.input_transforms:
            identifier_string = ""
            if transform.transform_id is not None:
                identifier_string = transform.short_transform_id()
                if transform.file is not None:
                    identifier_string = identifier_string + "/\"" + transform.file + "\""
            elif transform.file is not None:
                identifier_string = "\"" + transform.file + "\""
            else:
                identifier_string = "?"

            logger.info("#   {0}: {1} ({2})".format(transform.type,
                                                    identifier_string,
                                                    transform.description))
        for transform in self.aces_metadata_file.pipeline.look_transforms:
            identifier_string = ""
            if transform.transform_id is not None:
                identifier_string = transform.short_transform_id()
                if transform.file is not None:
                    identifier_string = identifier_string + "/\"" + transform.file + "\""
            elif transform.file is not None:
                identifier_string = "\"" + transform.file + "\""
            else:
                identifier_string = "?"

            logger.info("#   {0}: {1} ({2})".format(transform.type,
                                                    identifier_string,
                                                    transform.description))
        for transform in self.aces_metadata_file.pipeline.output_transforms:
            logger.info("#   {0}: {1} ({2})".format(transform.type,
                                                    transform.short_transform_id(),
                                                    transform.description))

        logger.info("\nCTLRENDER=`which ctlrender`\n")
        logger.info("if [ -z \"$1\" ] || [ -z \"$2\" ]")
        logger.info("then")
        logger.info("     echo \"Usage: [script name] path/to/input-file.[tiff|dpx|exr] path/to/output-file.[tiff|dpx|exr]\"")
        logger.info("     echo")
        logger.info("     exit 200")
        logger.info("fi\n")
        logger.info("INPUTIMAGEPATH=$1")
        logger.info("OUTPUTIMAGEPATH=$2\n")
        logger.info("export CTL_MODULE_PATH=\"{0}/utilities/\"\n".format(ctl_root_path))

        logger.info("$CTLRENDER \\")
        for transform in self.aces_metadata_file.pipeline.input_transforms:
            if transform.applied is False:
                self.log_transform_for_render(transform, ctl_root_path)
        for transform in self.aces_metadata_file.pipeline.look_transforms:
            if transform.applied is False:
                self.log_transform_for_render(transform, ctl_root_path)
        for transform in self.aces_metadata_file.pipeline.output_transforms:
            if transform.applied is False:
                self.log_transform_for_render(transform, ctl_root_path)
        logger.info("     -force \\")
        logger.info("     \"$INPUTIMAGEPATH\" \\")
        logger.info("     \"$OUTPUTIMAGEPATH\"\n")

        for transform in self.aces_metadata_file.pipeline.input_transforms:
            if transform.applied is True:
                self.log_transform_for_render(transform, ctl_root_path)
        for transform in self.aces_metadata_file.pipeline.output_transforms:
            if transform.applied is True:
                self.log_transform_for_render(transform, ctl_root_path)

        # logger.info("\n# -- end of script --\n")


    def log_transform_for_render(self, transform, ctl_root_path):
        if transform.applied is True:
            logger.info("# skipping {0} [applied=\"true\"]".format(transform.short_transform_id()))
        else:
            logger.info("     -ctl {0}/{1} \\".format(ctl_root_path, transform.relative_path))
            logger.info("     -param1 aIn 1.0 \\")
