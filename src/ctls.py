from src.amf import pass_context
from src.util import logger

from src.amf.amf import AmfFileReader
from src.ctl.ctl import TransformsTraverser
import click
import os


@click.command()
@click.argument('ctlrootpath', type=click.Path(exists=True, file_okay=False, readable=True))
@pass_context
def ctls(ctx, **kwargs):
    """Parse a folder with CTL files and print mapping between transformId and filepath."""
    ctx.load_args(**kwargs)

    traverser = TransformsTraverser(ctx.ctl_root_path)

    logger.info("Mappings:")
    traverser.log_ctl_mappings()
