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

sys.tracebacklimit = 0

@library(scope="GLOBAL", auto_keywords=True)
class PyocdLibrary():
    """Class to handle OCD requests over pyocd"""

    ROBOT_LIBRARY_SCOPE = "GLOBAL"
    ROBOT_AUTO_KEYWORDS = False

    def __init__(self):
        return

    @keyword("Reset")
    def reset(self):

        with ConnectHelper.session_with_chosen_probe() as session:
            while session.board.target.get_state() != Target.State.HALTED:
                pass

    @keyword("Load Firmware")
    def load_firmware(self, file: str):

        with ConnectHelper.session_with_chosen_probe() as session:
            flash = session.board.target.memory_map.get_boot_memory()
            # Load firmware into device.
            FileProgrammer(session).program(file)
            session.board.target.reset_and_halt()
            session.board.target.resume()


    @keyword("Resume")
    def resume(self):
        with ConnectHelper.session_with_chosen_probe() as session:
            session.board.target.resume()

__all__ = ["__version__", "PyocdLibrary"]
