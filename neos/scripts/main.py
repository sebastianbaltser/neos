import click
import pathlib

from neos.neos_server import Neos
from neos.submit_neos_job import create_neos_job


@click.group()
def neos():
    pass


@neos.command()
@click.argument("filenames", type=pathlib.Path, nargs=-1)
@click.option("--email", help="The email address to send the results to.")
@click.option("--category", default="lp", help="The solver category. Call `neos list categories` "
                                               "for a list of options.")
@click.option("--solver", default="CPLEX", help="The solver to use. Call `neos list solvers` "
                                                "for a list of options.")
@click.option("--priority", type=click.BOOL, default=False, help="Whether to submit to higher priority queue with "
                                                                 "maximum CPU time of 5 minutes.")
def submit(filenames, email, category, solver, priority):
    """
    Submit a job to NEOS for solving.

    FILENAME is the name of the files to be submitted. If passing only one single filename without an extension
    all files (.dat, .mod, and .run) must be in the same directory, and share the same name. If specifying multiple
    filenames, the extension should be included.
    """
    if len(filenames) not in (1, 3):
        click.echo(click.style("Either specify a single filename without extension or exactly three filenames.",
                               fg="red"))
        return
    if email is None:
        click.echo(click.style("Please specify an email address.", fg="red"))
        return
    create_neos_job(filenames, email, category, solver, priority)


@neos.group("list")
def list_options():
    pass


@list_options.command("categories")
def list_categories():
    """
    List the available solver categories.
    """
    categories = Neos().get_categories()
    click.echo(f"Categories available (abbreviation: category):")
    for abbreviation, category in categories.items():
        click.echo(f"{abbreviation}: {category}")


@list_options.command("solvers")
@click.option("--category", default="lp", help="The category to list solvers for.")
def list_solvers(category):
    """
    List the available solvers for a given category.
    """
    solvers = Neos().get_solvers(category)
    click.echo(f"Solvers available for category '{category}':")
    for solver in solvers:
        click.echo(solver)


if __name__ == '__main__':
    neos()
