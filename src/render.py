from src.amf import pass_context
from src.util import logger

from src.amf.amf import AmfFileReader
from src.ctl.ctl import TransformsTraverser
import click
import os


@click.command()
@click.argument('filepath', type=click.Path(exists=True))
@click.argument('ctlrootpath', type=click.Path(exists=True, file_okay=False, readable=True))
@click.option('--verbose', '-v', default=False, is_flag=True, help="Verbose output")
@pass_context
def render(ctx, **kwargs):
    """Read an AMF file at a given path and output a ctlrender command that renders the pipeline
    described in the AMF file."""
    ctx.load_args(**kwargs)

    if ctx.verbose:
        logger.info(f'render for \"{os.path.basename(ctx.filepath)}\"')

    traverser = TransformsTraverser(ctx.ctl_root_path)
    if ctx.verbose:
        traverser.log_ctls()

    reader = AmfFileReader(ctx.filepath)
    reader.parse()
    reader.log_render(traverser.transforms, traverser.root_path)
