#!/usr/bin/env python
import click
import src


@click.group()
def amf_cli():
    pass


amf_cli.add_command(src.info)
amf_cli.add_command(src.render)

if __name__ == '__main__':
    amf_cli()
