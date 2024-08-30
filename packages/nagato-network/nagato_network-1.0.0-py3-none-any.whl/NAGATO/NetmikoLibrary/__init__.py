"""
Copyright 2024 ITOCHU Techno-Solutions Corporation

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License."""

from robot.api.deco import library

from NAGATO.version import get_version

from ._wrapper import NetmikoWrapper
from .set_templates import set_templates

__all__ = ["NetmikoLibrary"]


@library
class NetmikoLibrary(NetmikoWrapper):
    """NetmikoLibrary is a Robot Framework library that provides SSH/Telnet connections to network devices and enables operations on the CLI.

    This library uses the netmiko package.
    """

    ROBOT_LIBRARY_SCOPE = "SUITE"
    ROBOT_LIBRARY_VERSION = get_version()

    def __init__(self):
        super().__init__()
        set_templates()
