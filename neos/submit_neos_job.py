import sys
import click

from neos.neos_server import Neos


def create_neos_job(filename, email, category, solver):
    neos = Neos()

    check_server_alive(neos)
    job_number, password = submit_job(neos, filename, email, category=category, solver=solver)
    click.echo(f"Job number: {job_number}")
    click.echo(f"Job password {password}")

    msg = neos.get_final_result(job_number, password)
    click.echo(click.style("Result received:", fg="green", bold=True))
    click.echo(msg.data.decode())


def check_server_alive(neos: Neos):
    if neos.is_server_alive():
        click.echo(click.style("Connected to the NEOS Server", fg="green"))
    else:
        click.echo("Could not make a connection to the NEOS Server", err=True)
        sys.exit(1)


def submit_job(neos, filename_base, email, **kwargs):
    job_description = create_neos_job_description(filename_base, email, **kwargs)

    click.echo("Submitting NEOS job")
    job_number, password = neos.submit_job(job_description)
    handle_error_response(job_number, password)
    return job_number, password


def create_neos_job_description(filename_base, email, **kwargs):
    files = read_ampl_files(filename_base)

    job_description = f"""
    <document>
        {"".join(f"<{option}>{value}</{option}>" for option, value in kwargs.items())}
        <inputMethod>AMPL</inputMethod>
        <email><![CDATA[{email}]]></email>
        <model><![CDATA[{files["model"]}]]></model>
        <data><![CDATA[{files["data"]}]]></data>
        <commands><![CDATA[{files["commands"]}]]></commands>
        <comments><![CDATA[]]></comments>
    </document>"""

    return job_description


def handle_error_response(job_number, password):
    if job_number == 0:
        click.echo(click.style("Job submission failed", fg="red", bold=True))
        click.echo(click.style("Error message:", fg="red", bold=True))
        click.echo(password)
        sys.exit(1)


def read_ampl_files(filename_base):
    file_type_extensions = {"model": "mod", "data": "dat", "commands": "run"}
    files = {}
    for file_type, extension in file_type_extensions.items():
        filename = f"{filename_base}.{extension}"
        click.echo(f"Reading file {filename}")
        with open(filename, "r") as file:
            files[file_type] = file.read()

    return files
