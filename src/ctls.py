from src.amf import pass_context
from src.util import logger

from src.amf.amf import AmfFileReader
from src.ctl.ctl import TransformsTraverser
import click
import os


@click.command()
@click.argument('ctlrootpath', type=click.Path(exists=True, file_okay=False, readable=True))
@click.argument('relativectlpath', required=False)

@pass_context
def ctls(ctx, **kwargs):
    """Parse a folder with CTL files and print mapping between transformId and filepath."""
    ctx.load_args(**kwargs)

    traverser = TransformsTraverser(ctx.ctl_root_path)

    if ctx.relativectlpath is None:
        #logger.info("Mappings:")
        traverser.log_ctl_mappings()
    else:
        #logger.info("... looking for {0}".format(ctx.relativectlpath))
        #traverser.log_ctl_mappings()
        transformId = traverser.transforms.transform_id_for_relative_path(ctx.relativectlpath)
        if transformId is None:
            logger.info("Couldn't find transformId for {0}".format(ctx.relativectlpath))
            exit(203)
        else:
            logger.info(transformId)
