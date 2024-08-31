<!--
SPDX-FileCopyrightText: 2024 Ledger SAS

SPDX-License-Identifier: Apache-2.0
-->

# robotframework-pyocd python package

This package is a ligthweight module to use the pyocd python API through robotframework tests so
that automated flash and test testsuites can be written for continuous deployment of embedded systems,
typically in a test farm.
This package uses the PyOCD tool, meaning that the JTAG interface is used in order to flash the target device.

When running the robotframework test suites, the device should be connected and a JTAG probe that delivers
the target reference (like, for example, ST-Link probes such as thoses of nucleo or disco boards).

This mean that Segger probes are not yet supported here as it requires a `target` variable to be passed
(see PyOCD documentation).

## Dependencies
 - Python >= 3.10
 - PyOCD >= 0.36.0
 - robotframework >= 7.0.0

## Usage

This library is built to be use through the `Library` directive of Robot-Framework and requires a probe uid
so that pyOCD is able to discriminate multiple probes being connected.

```robot
Library         PyocdLibrary    ${PROBE_UID}
```

By now, if the probe do not delivers a target identifier (like Segger probes), the pyOCD usage do not
allow a clean connection to the AP.
As a consequence, this small library do not support probe UID passing through robot ressource files.

The following basic command are defined:


### Probe Has Vcp

Return true if a VCP tty port has been found associated to the probe UID.

```robot
Probe Has Vcp
```

### Get Probe Vcp

Return the VCP tty name as a string, so that it can be used by other serial related robotframework
modules to get back the device serial Output.

```robot
Get Probe Vcp
```

### Load Firmware

Load a firmware into the connected target

Requires one argument: the firmware file path (string)

A typical usage is:

```robot
Load Firmware       builddir/firmware.hex
```

### Reset

Reset and hat the target. Target is halted when returned

A typical usage is:

```robot
Reset
```

### Resume

Resume a stopped target

A typical usage is:

```robot
Resume
```

## Example

A typical usage of this library is the followingr:

```robot
Library         SerialLibrary
Library         PyocdLibrary    ${PROBE_UID}

*** Test Cases ***

Load And Read From Serial
    Reset
    Load Firmware           ${FIRMWARE_PATH}
    ${vcp}                  Get Probe Vcp
    Log                     Virtual port is ${vcp}
    Connect                 ${vcp}    115200
    Set Timeout             20
    Resume
    Read All
```

## License
```
Copyright 2023 - 2024 Ledger SAS

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

 http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
```
