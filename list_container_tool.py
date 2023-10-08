import docker
from pydantic import BaseModel, Field
import logging
import traceback
from typing import Optional, List
# Adjust according to your actual import path
from superagi.tools.base_tool import BaseTool

# Configure logging
logging.basicConfig(filename='aptly.log', level=logging.ERROR,
                    format='%(asctime)s %(levelname)s: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

# Input validation model


class ListContainerInput(BaseModel):
    all: Optional[bool] = Field(
        False, description="Show all containers. Only running containers are shown by default.")
    filters: Optional[dict] = Field(
        None, description="Filters to process on the container list. E.g. {'status': ['created']}")

# Docker container listing tool


class ListContainerTool(BaseTool):
    def __init__(self, inputs: ListContainerInput):
        self.client = docker.from_env()
        self.inputs = inputs

    def list_containers(self):
        try:
            containers = self.client.containers.list(
                all=self.inputs.all, filters=self.inputs.filters)
            return containers  # Returns a list of container objects

        except docker.errors.APIError as e:
            logging.error(f"API error: {e}")
            logging.error(f"Stack trace: {traceback.format_exc()}")
        except Exception as e:  # Catch other types of exceptions
            logging.error(f"An unexpected error occurred: {e}")
            logging.error(f"Stack trace: {traceback.format_exc()}")

        return None  # Returning None or you can raise the error, or return an error message depending on your design
