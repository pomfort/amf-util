#!/usr/bin/env python
import click
import src


@click.group()
def amf_cli():
    pass


amf_cli.add_command(src.info)
amf_cli.add_command(src.render)
amf_cli.add_command(src.ctls)
#amf_cli.add_command(src.validate)

if __name__ == '__main__':
    amf_cli()
