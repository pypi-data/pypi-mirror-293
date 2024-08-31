# SPDX-License-Identifier: Apache-2.0
#
# Copyright 2023 Ledger SAS
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import sys
from .__version__ import __version__

from typing import Optional
from robot.api import logger, FatalError
from robot.api.deco import library, keyword
from robot.libraries.BuiltIn import BuiltIn
from pyocd.core.helpers import ConnectHelper
from pyocd.flash.file_programmer import FileProgrammer
import pyudev

sys.tracebacklimit = 0

@library(scope="GLOBAL", auto_keywords=False)
class PyocdLibrary():
    """Class to handle OCD requests over pyocd"""

    ROBOT_LIBRARY_SCOPE = "GLOBAL"
    ROBOT_AUTO_KEYWORDS = False

    def __init__(self, probeid: str):
        try:
            self._session = ConnectHelper.session_with_chosen_probe(unique_id = probeid)
            self._session.open()
        except error:
            print("Connection to probe failed in automatic way");
        self._probe_tty = None
        ctx = pyudev.Context()
        for dev in ctx.list_devices(subsystem='tty'):
            if dev.get('ID_SERIAL_SHORT') == probeid:
                self._probe_tty = dev.device_node
                break
        return

    @keyword("Get Probe Vcp")
    def get_vcp(self):
        return self._probe_tty

    @keyword("Probe Has Vcp")
    def has_vcp(self) -> bool:
        return bool(self._probe_tty is not None)

    @keyword("Reset")
    def reset(self):

        self._session.board.target.reset_and_halt()
        while self._session.board.target.get_state() != self._session.board.target.State.HALTED:
            pass

    @keyword("Load Firmware")
    def load_firmware(self, file: str):

        flash = self._session.board.target.memory_map.get_boot_memory()
        # Load firmware into device.
        FileProgrammer(self._session).program(file)
        self._session.board.target.reset_and_halt()

    @keyword("Resume")
    def resume(self):
        self._session.board.target.resume()


    def __del__(self):
        pass

__all__ = ["__version__", "PyocdLibrary"]
