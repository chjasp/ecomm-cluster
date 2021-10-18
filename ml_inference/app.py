import os
import shutil
import sys
from glob import glob
import base64
import click

from jina import Flow, Document, DocumentArray

from config import (
    max_docs,
    images_dir,
    backend_workdir,
    backend_port,
)
os.environ["JINA_WORKSPACE"] = backend_workdir
os.environ["JINA_PORT"] = str(backend_port)

def get_docs(max_docs=max_docs, images_dir=images_dir):
    docs = DocumentArray()
    print(f"Preparing {max_docs} Documents")
    img_files = glob(f'{images_dir}/*.jpg')
    
    for file in img_files[:max_docs]:
        # Uniform Resource Identifier
        doc = Document(uri=file)
        # this method loads the file into a np.ndarray 
        doc.convert_image_uri_to_blob()
        # tags can be used to store any other random data you'd need
        doc.tags['filename'] = file
        docs.append(doc)
    return docs

def encode_image_to_base64(image_file):
    with open(image_file, "rb") as file:
        encoded_image = base64.b64encode(file.read())
        encoded_image = str(encoded_image)


def index(input_docs, num_docs: int = max_docs):
    with Flow.load_config("flows/flow.yml") as flow:
        flow.post(
            on="/index",
            inputs=input_docs,
            request_size=64,
            read_mode="rb",
        )


def query():
    # Starts the restful query API
    flow = Flow.load_config("flows/flow.yml")
    flow.port = backend_port
    flow.protocol = 'http'
    with flow:
        flow.block()



@click.command()
@click.option(
    "--task",
    "-t",
    type=click.Choice(["index", "query"], case_sensitive=False),
)
@click.option("--num_docs", "-n", default=max_docs)
@click.option("--data_dir", "-dir", default=images_dir)
@click.option("--force", "-f", is_flag=True)
def main(task: str, num_docs: int, data_dir:str, force: bool):
    workspace = os.environ["JINA_WORKSPACE"]
    if task == "index":
        if os.path.exists(workspace):
            if force:
                shutil.rmtree(workspace)
            else:
                print(
                    f"The directory {workspace} already exists. Please remove it before indexing again."
                )
                sys.exit(1)
        docs = get_docs(max_docs=num_docs, images_dir=data_dir)
        index(docs, num_docs)
    if task == "query":
        if not os.path.exists(workspace):
            print(
                f"The directory {workspace} does not exist. Please index first via `python app.py -t index`"
            )
            sys.exit(1)
        query()


if __name__ == "__main__":
    main()

