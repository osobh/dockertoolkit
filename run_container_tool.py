import docker
from pydantic import BaseModel, Field
import logging
import traceback
from typing import Optional, List, Dict
# Adjust according to your actual import path
from superagi.tools.base_tool import BaseTool

# Configure logging
logging.basicConfig(filename='aptly.log', level=logging.ERROR,
                    format='%(asctime)s %(levelname)s: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

# Input validation model


class RunContainerInput(BaseModel):
    image: str = Field(..., description="The name of the image to run")
    command: Optional[List[str]] = Field(
        None, description="The command to run in the container")
    name: Optional[str] = Field(None, description="A name for the container")
    volumes: Optional[Dict[str, Dict]] = Field(
        None, description="Volumes to mount into the container, similar to the -v option in docker run")
    detach: bool = Field(True, description="Run container in the background")

# Docker container running tool


class RunContainerTool(BaseTool):
    def __init__(self, inputs: RunContainerInput):
        self.client = docker.from_env()
        self.inputs = inputs

    def run_container(self):
        try:
            container = self.client.containers.run(
                image=self.inputs.image,
                command=self.inputs.command,
                name=self.inputs.name,
                volumes=self.inputs.volumes,
                detach=self.inputs.detach
            )

            return container  # Returns a container object

        except docker.errors.ImageNotFound as e:
            logging.error(f"Image not found error: {e}")
            logging.error(f"Stack trace: {traceback.format_exc()}")
        except docker.errors.APIError as e:
            logging.error(f"API error: {e}")
            logging.error(f"Stack trace: {traceback.format_exc()}")
        except Exception as e:  # Catch other types of exceptions
            logging.error(f"An unexpected error occurred: {e}")
            logging.error(f"Stack trace: {traceback.format_exc()}")

        return None  # Returning None or you can raise the error, or return an error message depending on your design
