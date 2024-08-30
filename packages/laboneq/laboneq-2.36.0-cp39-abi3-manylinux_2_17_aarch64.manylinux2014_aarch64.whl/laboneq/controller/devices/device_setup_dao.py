# Copyright 2022 Zurich Instruments AG
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import copy
import logging
import math
from typing import TYPE_CHECKING, ItemsView, Iterator

from laboneq.controller.communication import ServerQualifier
from laboneq.controller.devices.device_zi import DeviceOptions, DeviceQualifier
from laboneq.controller.versioning import SetupCaps
from laboneq.data.execution_payload import (
    TargetChannelCalibration,
    TargetChannelType,
    TargetDeviceType,
)

if TYPE_CHECKING:
    from laboneq.data.execution_payload import TargetDevice, TargetServer, TargetSetup

_logger = logging.getLogger(__name__)


def _make_server_qualifier(server: TargetServer, ignore_version_mismatch: bool):
    return ServerQualifier(
        host=server.host,
        port=server.port,
        ignore_version_mismatch=ignore_version_mismatch,
    )


def _make_device_qualifier(
    target_device: TargetDevice, has_shf: bool
) -> DeviceQualifier:
    driver = target_device.device_type.name
    options = DeviceOptions(
        serial=target_device.device_serial,
        interface=target_device.interface,
        dev_type=target_device.device_type.name,
        is_qc=target_device.is_qc,
        qc_with_qa=target_device.qc_with_qa,
        gen2=has_shf,
        reference_clock_source=target_device.reference_clock_source,
        expected_installed_options=target_device.device_options,
    )
    if not target_device.has_signals and not target_device.internal_connections:
        # Treat devices without defined connections as non-QC
        driver = "NONQC"
        if options.is_qc is None:
            options.is_qc = False

    return DeviceQualifier(
        uid=target_device.uid,
        server_uid=target_device.server.uid,
        driver=driver,
        options=options,
    )


class DeviceSetupDAO:
    def __init__(
        self,
        target_setup: TargetSetup,
        setup_caps: SetupCaps,
        ignore_version_mismatch: bool = False,
    ):
        self._target_setup = target_setup
        self._servers: dict[str, ServerQualifier] = {
            server.uid: _make_server_qualifier(
                server=server,
                ignore_version_mismatch=ignore_version_mismatch,
            )
            for server in target_setup.servers
        }

        has_shf = False
        self._has_uhf = False
        self._has_qhub = False
        for device in target_setup.devices:
            if device.device_type in (
                TargetDeviceType.SHFQA,
                TargetDeviceType.SHFSG,
            ):
                has_shf = True
            if device.device_type == TargetDeviceType.UHFQA:
                self._has_uhf = True
            if device.device_type == TargetDeviceType.QHUB:
                self._has_qhub = True

        self._devices: list[DeviceQualifier] = [
            _make_device_qualifier(target_device=device, has_shf=has_shf)
            for device in target_setup.devices
        ]
        self._used_outputs: dict[str, dict[str, list[int]]] = {
            device.uid: device.connected_outputs for device in target_setup.devices
        }
        self._downlinks: dict[str, list[tuple[str, str]]] = {
            device.uid: [i for i in device.internal_connections]
            for device in target_setup.devices
        }
        self._calibrations: dict[str, list[TargetChannelCalibration]] = {
            device.uid: copy.deepcopy(device.calibrations)
            for device in target_setup.devices
        }

        self._setup_caps = setup_caps

    @property
    def servers(self) -> ItemsView[str, ServerQualifier]:
        return self._servers.items()

    @property
    def instruments(self) -> Iterator[DeviceQualifier]:
        return iter(self._devices)

    @property
    def has_uhf(self) -> bool:
        return self._has_uhf

    @property
    def has_qhub(self) -> bool:
        return self._has_qhub

    def downlinks_by_device_uid(self, device_uid: str) -> list[tuple[str, str]]:
        return self._downlinks[device_uid]

    def resolve_ls_path_outputs(self, ls_path: str) -> tuple[str | None, set[int]]:
        for device_uid, used_outputs in self._used_outputs.items():
            outputs = used_outputs.get(ls_path)
            if outputs:
                return device_uid, set(outputs)
        return None, set()

    def get_device_used_outputs(self, device_uid: str) -> set[int]:
        used_outputs: set[int] = set()
        for sig_used_outputs in self._used_outputs[device_uid].values():
            used_outputs.update(sig_used_outputs)
        return used_outputs

    def get_device_rf_voltage_offsets(self, device_uid: str) -> dict[int, float]:
        """Returns map: <sigout index> -> <voltage_offset>"""
        voltage_offsets: dict[int, float] = {}

        def add_voltage_offset(sigout: int, voltage_offset: float):
            if sigout in voltage_offsets:
                if not math.isclose(voltage_offsets[sigout], voltage_offset):
                    _logger.warning(
                        "Ambiguous 'voltage_offset' for the output %s of device %s: %s != %s, "
                        "will use %s",
                        sigout,
                        device_uid,
                        voltage_offsets[sigout],
                        voltage_offset,
                        voltage_offsets[sigout],
                    )
            else:
                voltage_offsets[sigout] = voltage_offset

        for calib in self._calibrations.get(device_uid) or []:
            if calib.channel_type == TargetChannelType.RF and len(calib.ports) == 1:
                port_parts = calib.ports[0].upper().split("/")
                if len(port_parts) == 2 and port_parts[0] == "SIGOUTS":
                    sigout = int(port_parts[1])
                elif (
                    len(port_parts) == 3
                    and port_parts[0] in ["SGCHANNELS", "QACHANNELS"]
                    and port_parts[2] == "OUTPUT"
                ):
                    sigout = int(port_parts[1])
                else:
                    sigout = None
                if sigout is not None:
                    add_voltage_offset(sigout, calib.voltage_offset)
        return voltage_offsets

    @property
    def setup_caps(self):
        return self._setup_caps
