import docker
from pydantic import BaseModel, Field
import logging
import traceback
from typing import Optional
# Adjust according to your actual import path
from superagi.tools.base_tool import BaseTool

# Configure logging
logging.basicConfig(filename='aptly.log', level=logging.ERROR,
                    format='%(asctime)s %(levelname)s: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

# Input validation model


class DeleteContainerInput(BaseModel):
    container_id: str = Field(...,
                              description="The ID or name of the container to delete")
    force: Optional[bool] = Field(
        False, description="Force the removal of a running container (equivalent to the --force option in docker rm)")
    v: Optional[bool] = Field(
        False, description="Remove the volumes associated with the container")

# Docker container deletion tool


class DeleteContainerTool(BaseTool):
    def __init__(self, inputs: DeleteContainerInput):
        self.client = docker.from_env()
        self.inputs = inputs

    def delete_container(self):
        try:
            container = self.client.containers.get(self.inputs.container_id)
            container.remove(force=self.inputs.force, v=self.inputs.v)
            logging.info(
                f"Container {self.inputs.container_id} removed successfully.")

        except docker.errors.NotFound as e:
            logging.error(f"Container not found error: {e}")
            logging.error(f"Stack trace: {traceback.format_exc()}")
            return "Container not found"
        except docker.errors.APIError as e:
            logging.error(f"API error: {e}")
            logging.error(f"Stack trace: {traceback.format_exc()}")
            return "API error"
        except Exception as e:  # Catch other types of exceptions
            logging.error(f"An unexpected error occurred: {e}")
            logging.error(f"Stack trace: {traceback.format_exc()}")
            return "Unexpected error"

        return "Container removed successfully"  # Successful removal
