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

This library is built to be use through the `Library` directive of Robot-Framework:

```robot
Library         PyocdLibrary
```

It is considered that the pyocd local configuration is made so that the probe is automatically selected in
case of multiple probes connected to the host.
This can be done at pyocd local through pyocd configuration (see https://pyocd.io/docs/configuration.html).

As a consequence, this small library do not support probe UID passing through robot ressource files.

The following basic command are defined:

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
