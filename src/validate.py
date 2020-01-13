from src.amf import pass_context
from src.util import logger
from lxml import etree

from src.amf.amf import AmfFileReader
import click
import os


@click.command()
@click.argument('filepath', type=click.Path(exists=True))
@click.argument('schemapath', type=click.Path(exists=True))

@pass_context
def validate(ctx, **kwargs):
    """Validate an AMF file against xsd schema."""
    ctx.load_args(**kwargs)

    amf_filepath = ctx.filepath
    schema_filepath = ctx.schemapath

    xmlschema_doc = etree.parse(schema_filepath)
    xmlschema = etree.XMLSchema(xmlschema_doc)

    amf_doc = etree.parse(amf_filepath)
    result = xmlschema.validate(amf_doc)

    if result:
        logger.error("OK: {0}".format(amf_filepath))
    else:
        logger.error("ERROR: {0} didn't validate against {1}!".format(amf_filepath, schema_filepath))
        logger.info("Issues:\n{}".format(xmlschema.error_log))
        exit(201)   # amfutil_error_xsd_validation_failed
