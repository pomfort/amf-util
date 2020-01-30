"""
__author__ = "Patrick Renner"
__copyright__ = "Copyright 2020, Pomfort GmbH"

__license__ = "MIT"
__maintainer__ = "Patrick Renner"
__email__ = "opensource@pomfort.com"
"""

from src.amf import pass_context
from src.util import logger

from src.amf.amf import AmfFileReader
import click
import os


@click.command()
@click.argument('filepath', type=click.Path(exists=True))
@click.option('--compact', '-c', default=False, is_flag=True, help="Compact, single-line output")
@click.option('--verbose', '-v', default=False, is_flag=True, help="Verbose output")
@pass_context
def info(ctx, **kwargs):
    """Read an AMF file at a given path and display information about the contents of the file."""
    ctx.load_args(**kwargs)

    if ctx.verbose:
        logger.info(f'info for \"{os.path.basename(ctx.filepath)}\"')

    reader = AmfFileReader(ctx.filepath)
    reader.log_info()
