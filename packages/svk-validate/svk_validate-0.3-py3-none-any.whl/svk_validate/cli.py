import click
from svk_validate.validate import ErmsValidator


@click.group()
@click.version_option()
def cli():
    """A simple tool for validating XML-files against Church of Sweden's adaptation of ERMS."""


@cli.command(name="vxml")
@click.argument('filename', type=click.Path(exists=True))
@click.option("--logfile", is_flag=True, help="Write log to file.")
def vxml(filename, logfile):
    """Validate an ERMS-SVK XML-file"""
    val = ErmsValidator(filename)
    val.validate(logfile)
