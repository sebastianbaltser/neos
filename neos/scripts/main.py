import click
from neos.neos_server import Neos
from neos.submit_neos_job import create_neos_job


@click.group()
def neos():
    pass


@neos.command()
@click.argument('filename')
@click.argument("email")
@click.option("--category", default="lp", help="The solver category. Call neos list categories for a list of options.")
@click.option("--solver", default="CPLEX", help="The solver to use. Call `neos list solvers` for a list of options.")
def submit(filename, email, category, solver):
    """
    Submit a job to NEOS for solving.

    FILENAME is the name of the files to be submitted without the extension. The files must be in the same directory,
    and share the same name.
    EMAIL is the email address to send the results to.
    """
    create_neos_job(filename, email, category, solver)


@neos.command("list-categories")
def list_category():
    """
    List the available solver categories.
    """
    categories = Neos().get_categories()
    click.echo(f"Categories available (abbreviation: category):")
    for abbreviation, category in categories.items():
        click.echo(f"{abbreviation}: {category}")


@neos.command("list-solvers")
@click.option("--category", default="lp", help="The category to list solvers for.")
def list_solvers(category):
    """
    List the available solvers.
    """
    solvers = Neos().get_solvers(category)
    click.echo(f"Solvers available for category '{category}':")
    for solver in solvers:
        click.echo(solver)


if __name__ == '__main__':
    neos()
