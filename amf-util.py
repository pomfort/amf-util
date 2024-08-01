#!/usr/bin/env python3
"""
__author__ = "Patrick Renner"
__copyright__ = "Copyright 2020, Pomfort GmbH"

__license__ = "MIT"
__maintainer__ = "Patrick Renner"
__email__ = "opensource@pomfort.com"
"""

import click
import src


@click.group()
def amf_cli():
    pass


amf_cli.add_command(src.info)
amf_cli.add_command(src.render)
amf_cli.add_command(src.ctls)

if __name__ == '__main__':
    amf_cli()
