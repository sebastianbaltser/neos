import sys
import click
import time
import itertools

from neos.neos_server import Neos


def create_neos_job(filenames, email, category, solver):
    job_description = create_neos_job_description(filenames, email, category=category, solver=solver)

    neos = Neos()
    check_server_alive(neos)
    job_number, password = submit_job(neos, job_description)
    click.echo(f"Job number: {job_number}")
    click.echo(f"Job password {password}")

    result = get_result(neos, job_number, password)
    click.echo(click.style("Result received:", fg="green", bold=True))
    click.echo(result)


def check_server_alive(neos: Neos):
    if neos.is_server_alive():
        click.echo(click.style("Connected to the NEOS Server", fg="green"))
    else:
        click.echo("Could not make a connection to the NEOS Server", err=True)
        sys.exit(1)


def submit_job(neos, job_description):
    click.echo("Submitting NEOS job")
    job_number, password = neos.submit_job(job_description)
    handle_error_response(job_number, password)
    return job_number, password


def create_neos_job_description(filenames, email, **kwargs):
    model, data, commands = read_ampl_files(*handle_filenames(filenames))

    job_description = f"""
    <document>
        {"".join(f"<{option}>{value}</{option}>" for option, value in kwargs.items())}
        <inputMethod>AMPL</inputMethod>
        <email><![CDATA[{email}]]></email>
        <model><![CDATA[{model}]]></model>
        <data><![CDATA[{data}]]></data>
        <commands><![CDATA[{commands}]]></commands>
        <comments><![CDATA[]]></comments>
    </document>"""

    return job_description


def handle_error_response(job_number, password):
    if job_number == 0:
        click.echo(click.style("Job submission failed", fg="red", bold=True))
        click.echo(click.style("Error message:", fg="red", bold=True))
        click.echo(password)
        sys.exit(1)


def handle_filenames(filenames):
    """
    Return names of model-, data- and command-files in that order.

    Parameters:
        filenames (pathlib.Path | list[pathlib.Path]: Single filename or list of filenames

    Returns:
        (pathlib.Path, pathlib.Path, pathlib.Path): model-, data- and command-files in that order
    """
    suffixes = [".mod", ".dat", ".run"]
    if len(filenames) == 1:
        return (filenames[0].with_suffix(suffix) for suffix in suffixes)
    else:
        try:
            return sorted(filenames, key=lambda x: suffixes.index(x.suffix))
        except ValueError:
            click.echo(click.style(f"Invalid filename.", fg="red", bold=True))


def read_ampl_files(model, data, commands):
    files = []
    for filename in (model, data, commands):
        click.echo(f"Reading file {filename}")
        with open(filename, "r") as file:
            files.append(file.read())

    return files


def get_result(neos, job_id, password):
    loading = itertools.cycle(["", ".", "..", "..."])
    while True:
        status = neos.get_job_status(job_id, password)
        click.echo(f"  Status: {status} " + next(loading) + " "*20 + "\r", nl=False)
        if status == "Done":
            click.echo("")
            break
        time.sleep(0.5)

    return neos.get_final_result(job_id, password).data.decode()
