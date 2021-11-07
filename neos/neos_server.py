import sys
import click
import xmlrpc.client as xmlrpclib


def create_neos_server():
    click.echo("Connecting to NEOS Server")
    return xmlrpclib.ServerProxy("https://neos-server.org:3333")


class Neos:
    def __init__(self):
        self.server = create_neos_server()

    def is_server_alive(self):
        alive = self.server.ping()
        return alive == "NeosServer is alive\n"

    def submit_job(self, payload):
        return self.server.submitJob(payload)

    def get_final_result(self, job_id, password):
        return self.server.getFinalResults(job_id, password)

    def get_solvers(self, category):
        return self.server.listSolversInCategory(category)

    def get_categories(self):
        return self.server.listCategories()

    def get_job_status(self, job_id, password) -> str:
        """
        Gets the current status of the job. Returns "Done", "Running", "Waiting".

        Raises:
            ValueError: If the job is not found or the password is incorrect.
        """
        response = self.server.getJobStatus(job_id, password)
        if response == "Unknown Job":
            raise ValueError(f"Unknown Job ID: {job_id}")
        elif response == "Bad Password":
            raise ValueError(f"Bad Password '{password}' for Job ID: {job_id}")
        else:
            return response
