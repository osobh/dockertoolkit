import os
import docker
import logging
import traceback  # Added for improved error logging
from typing import Dict, List, Optional, Type
from pydantic import BaseModel, Field
# Adjust according to your actual import path
from superagi.tools.base_tool import BaseTool

# Configure logging
logging.basicConfig(filename='aptly.log', level=logging.ERROR,
                    format='%(asctime)s %(levelname)s: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')


class ListBuildInput(BaseModel):
    path: Optional[str] = Field(
        None, description="Path to the directory containing the Dockerfile")
    fileobj: Optional[str] = Field(
        None, description="A file object to use as the Dockerfile. (Or a file-like object)")
    tag: Optional[str] = Field(
        None, description="A tag to add to the final image")
    quiet: bool = Field(False, description="Whether to return the status")
    nocache: bool = Field(
        False, description="Don't use the cache when set to True")
    rm: bool = Field(True, description="Remove intermediate containers")
    timeout: Optional[int] = Field(None, description="HTTP timeout")
    custom_context: bool = Field(
        False, description="Optional if using fileobj")
    encoding: Optional[str] = Field(
        None, description="The encoding for a stream")
    pull: bool = Field(
        False, description="Downloads any updates to the FROM image in Dockerfiles")
    forcerm: bool = Field(
        False, description="Always remove intermediate containers")
    dockerfile: Optional[str] = Field(
        None, description="Path within the build context to the Dockerfile")
    buildargs: Optional[Dict[str, str]] = Field(
        None, description="A dictionary of build arguments")
    container_limits: Optional[Dict[str, str]] = Field(
        None, description="A dictionary of limits applied to each container created by the build process")
    shmsize: Optional[int] = Field(
        None, description="Size of /dev/shm in bytes")
    labels: Optional[Dict[str, str]] = Field(
        None, description="A dictionary of labels to set on the image")
    cache_from: Optional[List[str]] = Field(
        None, description="A list of images used for build cache resolution")
    target: Optional[str] = Field(
        None, description="Name of the build-stage to build in a multi-stage Dockerfile")
    network_mode: Optional[str] = Field(
        None, description="Networking mode for the run commands during build")
    squash: Optional[bool] = Field(
        None, description="Squash the resulting images layers into a single layer")
    extra_hosts: Optional[Dict[str, str]] = Field(
        None, description="Extra hosts to add to /etc/hosts in building containers")
    platform: Optional[str] = Field(
        None, description="Platform in the format os[/arch[/variant]]")
    isolation: Optional[str] = Field(
        None, description="Isolation technology used during build")
    use_config_proxy: Optional[bool] = Field(
        None, description="Use proxy from Docker client configuration file")


class BuildContainerTool(BaseTool):
    def __init__(self, inputs: ListBuildInput):
        self.client = docker.from_env()
        self.inputs = inputs

    def build_image(self):
        try:
            image, logs = self.client.images.build(
                path=self.inputs.path,
                fileobj=self.inputs.fileobj,
                tag=self.inputs.tag,
                quiet=self.inputs.quiet,
                nocache=self.inputs.nocache,
                rm=self.inputs.rm,
                timeout=self.inputs.timeout,
                custom_context=self.inputs.custom_context,
                encoding=self.inputs.encoding,
                pull=self.inputs.pull,
                forcerm=self.inputs.forcerm,
                dockerfile=self.inputs.dockerfile,
                buildargs=self.inputs.buildargs,
                container_limits=self.inputs.container_limits,
                shmsize=self.inputs.shmsize,
                labels=self.inputs.labels,
                cache_from=self.inputs.cache_from,
                target=self.inputs.target,
                network_mode=self.inputs.network_mode,
                squash=self.inputs.squash,
                extra_hosts=self.inputs.extra_hosts,
                platform=self.inputs.platform,
                isolation=self.inputs.isolation,
                use_config_proxy=self.inputs.use_config_proxy
            )

            return image, logs

        except errors.BuildError as e:
            logging.error(f"Build error: {e}")
            logging.error(f"Stack trace: {traceback.format_exc()}")
        except errors.APIError as e:
            logging.error(f"API error: {e}")
            logging.error(f"Stack trace: {traceback.format_exc()}")
        except TypeError as e:
            logging.error(f"Type error: {e}")
            logging.error(f"Stack trace: {traceback.format_exc()}")

        # Consider adding return statements to handle errors gracefully
        return None
