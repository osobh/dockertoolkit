import docker
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
import logging
import traceback
from superagi.tools.base_tool import BaseTool  # Adjust according to your actual import path

# Configure logging
logging.basicConfig(filename='aptly.log', level=logging.ERROR,
                    format='%(asctime)s %(levelname)s: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

# Input validation model
class StartContainerInput(BaseModel):
    container_id: str = Field(..., description="The ID or name of the container to start")
    detach_keys: Optional[str] = Field(None, description="Override the key sequence for detaching a container")

# Docker container starting tool
class StartContainerTool(BaseTool):
    def __init__(self, inputs: StartContainerInput):
        self.client = docker.from_env()
        self.inputs = inputs

    def start_container(self):
        try:
            container = self.client.containers.get(self.inputs.container_id)
            response = container.start(detach_keys=self.inputs.detach_keys)
            return response  # In this context, a None response often means the operation was successful
            
        except docker.errors.NotFound as e:
            logging.error(f"Container not found error: {e}")
            logging.error(f"Stack trace: {traceback.format_exc()}")
        except docker.errors.APIError as e:
            logging.error(f"API error: {e}")
            logging.error(f"Stack trace: {traceback.format_exc()}")
        except Exception as e:  # Catch other types of exceptions
            logging.error(f"An unexpected error occurred: {e}")
            logging.error(f"Stack trace: {traceback.format_exc()}")

        return None  # Returning None or you can raise the error, or return an error message depending on your design
