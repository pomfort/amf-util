from src.amf import pass_context
from src.util import logger

from src.amf.amf import AmfFileReader
from src.ctl.ctl import TransformsTraverser
import click
import os


@click.command()
@click.argument('ctlrootpath', type=click.Path(exists=True, file_okay=False, readable=True))
@click.argument('relativectlpath', required=False)
@click.option('--description', '-d', default=False, is_flag=True, help="Output description instead of transformId")
@click.option('--verbose', '-v', default=False, is_flag=True, help="Verbose output")

@pass_context
def ctls(ctx, **kwargs):
    """Parse a folder with CTL files and print mapping between transformId and filepath."""
    ctx.load_args(**kwargs)

    if ctx.relativectlpath is None:
        #logger.info("Mappings:")
        ctx.verbose = True  # show errors while traversing
        traverser = TransformsTraverser(ctx.ctl_root_path)

        traverser.log_ctl_mappings()
    else:
        #logger.info("... looking for {0}".format(ctx.relativectlpath))
        #traverser.log_ctl_mappings()

        traverser = TransformsTraverser(ctx.ctl_root_path)

        transformId = traverser.transforms.transform_id_for_relative_path(ctx.relativectlpath)
        if ctx.description:
            if transformId is None:
                if ctx.verbose == True:
                    logger.error("Couldn't find description for relative path {0}".format(ctx.relativectlpath))
                exit(203)
            else:
                description = traverser.transforms.description_for_relative_path(ctx.relativectlpath)
                logger.info(description)
        else:
            if transformId is None:
                if ctx.verbose == True:
                    logger.error("Couldn't find transformId for relative path {0}".format(ctx.relativectlpath))
                exit(203)
            else:
                logger.info(transformId)
