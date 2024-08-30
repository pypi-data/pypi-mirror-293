from pathlib import Path

import docker
import requests

from breba_docs.analyzer.service import analyze
from breba_docs.services.openai_agent import OpenAIAgent
from dotenv import load_dotenv
from urllib.parse import urlparse

DEFAULT_LOCATION = ("https://gist.githubusercontent.com/yasonk/16990780a6b6e46163d1caf743f38e8f/raw"
                    "/6d5fbb7e7053642f45cb449ace1adb4eea38e6de/gistfile1.txt")


def is_valid_url(url):
    # TODO: check if md file
    parsed_url = urlparse(url)

    return all([parsed_url.scheme, parsed_url.netloc])


def is_file_path(file_path):
    path = Path(file_path)
    return path.is_file()


def run():
    load_dotenv()
    client = docker.from_env()
    started_container = client.containers.run(
        "python:3",
        command="/bin/bash",
        stdin_open=True,
        tty=True,
        detach=True,
        working_dir="/usr/src",
    )

    doc_location = input("Provide url to doc file or an absolute path:") or DEFAULT_LOCATION

    errors = []
    if is_file_path(doc_location):
        with open(doc_location, "r") as file:
            document = file.read()
    elif is_valid_url(doc_location):
        response = requests.get(doc_location)
        # TODO: if response is not md file produce error message
        document = response.text
    else:
        document = None
        errors.append("Not a valid url or local file path")

    if errors:
        for error in errors:
            print(error)
    elif document:
        ai_agent = OpenAIAgent()
        analyze(ai_agent, started_container, document)
    else:
        print("Document text is empty, but no errors were found")


if __name__ == "__main__":
    run()
