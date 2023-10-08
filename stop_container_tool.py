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


class StopContainerInput(BaseModel):
    container_id: str = Field(...,
                              description="The ID or name of the container to stop")
    timeout: Optional[int] = Field(
        10, description="Timeout to wait for the container to stop before sending a SIGKILL")

# Docker container stopping tool


class StopContainerTool(BaseTool):
    def __init__(self, inputs: StopContainerInput):
        self.client = docker.from_env()
        self.inputs = inputs

    def stop_container(self):
        try:
            container = self.client.containers.get(self.inputs.container_id)
            response = container.stop(timeout=self.inputs.timeout)
            return response  # Similar to start, a None response often means the operation was successful

        except docker.errors.NotFound as e:
            logging.error(f"Container not found error: {e}")
            logging.error(f"Stack trace: {traceback.format_exc()}")
        except docker.errors.APIError as e:
            logging.error(f"API error: {e}")
            logging.error(f"Stack trace: {traceback.format_exc()}")
        except Exception as e:  # Catch other types of exceptions
            logging.error(f"An unexpected error occurred: {e}")
            logging.error(f"Stack trace: {traceback.format_exc()}")

        return None  # Returning None, or you can raise the error, or return an error message depending on your design
