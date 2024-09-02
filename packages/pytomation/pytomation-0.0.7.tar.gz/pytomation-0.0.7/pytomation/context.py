import logging
from pathlib import Path
from typing import TYPE_CHECKING, Any, Dict, List

from pytomation.file_builder.file_builder import FileBuilder
from pytomation.file_builder.local_file_builder import LocalFileBuilder
from pytomation.utils import command

if TYPE_CHECKING:
    from pytomation.app import App
    from pytomation.module import Module
    from pytomation.plugin import Plugin
    from pytomation.profile import Profile


# TODO: Context with no sense! Please, make a twist and fix this mess!
class Context:

    @staticmethod
    def from_dict(kwargs: Dict):
        return Context(**kwargs)

    def __init__(
        self,
        app: "App",
        profile: "Profile",
        args: List[str],
        current_module: "Module",
        plugins: Dict[str, "Plugin"],
        **ignore,
    ):
        self.app = app
        self.args = args
        self.profile = profile
        self.current_module = current_module
        self.base_module = current_module
        self.root_module = current_module.root_module
        self.plugins = plugins

    @property
    def path(self) -> Path:
        return self.current_module.path

    def build_path(self, name) -> Path:
        return self.path.joinpath(name)

    def copy(self):
        return Context.from_dict(self.__dict__)

    def extend_from_module(self, module: "Module"):
        copy = self.copy()
        copy.current_module = module
        return copy

    def run_command(self, *cmd: any, timeout=None, check=True):
        logging.debug(f"Running command: %s, {timeout}, {check}", cmd)
        return command.run(self.path, *cmd, timeout=timeout, check=check)

    def run_action_on_module(self, module_path: str, action: str):
        logging.debug(f"Running action on module: {module_path}:{action}")
        self.app.run_action_on_module(module_path, action)

    def get_file_builder(self) -> FileBuilder:
        return LocalFileBuilder(self.path)

    def get_plugin(self, name: str) -> Any:
        return self.plugins[name].build(self)
