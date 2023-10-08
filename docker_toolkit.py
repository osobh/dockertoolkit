from abc import ABC
from typing import Type, List
from superagi.tools.base_tool import BaseTool, BaseToolkit, ToolConfiguration
from superagi.tools.docker.build_container_tool import BuildContainerTool
from superagi.tools.docker.start_container_tool import StartContainerTool
from superagi.tools.docker.stop_container_tool import StopContainerTool
from superagi.tools.docker.run_container_tool import RunContainerTool
from superagi.tools.docker.list_container_tool import ListContainerTool
from superagi.tools.docker.delete_container_tool import DeleteContainerTool
from superagi.types.key_type import ToolConfigKeyType


class DockerToolkit(BaseToolkit, ABC):
    name: str = "Docker Toolkit"
    description: str = "Docker Toolkit contains all tools related to Docker"

    def get_tools(self) -> List[BaseTool]:
        return [BuildContainerTool(), StartContainerTool(), StopContainerTool(), RunContainerTool(), ListContainerTool(), DeleteContainerTool()]

    def get_env_keys(self) -> List[ToolConfiguration]:
        return [
            ToolConfiguration(
                key="DOCKER_IMAGE", key_type=ToolConfigKeyType.STRING, is_required=True, is_secret=False),
            ToolConfiguration(
                key="DOCKER_TAG", key_type=ToolConfigKeyType.STRING, is_required=True, is_secret=False),
            ToolConfiguration(
                key="DOCKER_HOST", key_type=ToolConfigKeyType.STRING, is_required=True, is_secret=False),
            ToolConfiguration(
                key="DOCKER_PORT", key_type=ToolConfigKeyType.STRING, is_required=True, is_secret=False)
        ]
