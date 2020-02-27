# SPDX-License-Identifier: MIT

import fcntl
import logging
import libevdev
import os
import struct
import time
import typing

import hidtools.uhid

from typing import List

if typing.TYPE_CHECKING:
    from ratbag_emu.device import Device  # pragma: no cover


class Endpoint(hidtools.uhid.UHIDDevice):
    '''
    Represents a device endpoint

    A HID device is created for each endpoint. The enpoint can be used to
    receive and send data

    :param owner:   Endpoint owner
    :param rdesc:   Report descriptor
    :param number:  Endpoint number
    '''

    input_type_mapping = {
        'ID_INPUT_TOUCHSCREEN': 'Touch Screen',
        'ID_INPUT_TOUCHPAD': 'Touch Pad',
        'ID_INPUT_TABLET': 'Pen',
        'ID_INPUT_MOUSE': 'Mouse',
        'ID_INPUT_KEY': 'Key',
        'ID_INPUT_JOYSTICK': 'Joystick',
        'ID_INPUT_ACCELEROMETER': 'Accelerometer',
    }

    def __init__(self, owner: 'Device', rdesc: List[int], number: int):
        super().__init__()

        self.__logger = logging.getLogger('ratbag-emu.endpoint')

        self._owner = owner

        self._info = owner.info
        self.rdesc = rdesc
        self.number = number
        self.name = f'ratbag-emu {owner.id} ({owner.name}, {self.vid:04x}:{self.pid:04x}, {self.number})'
        self._opened_files = []
        self.input_nodes = {}

        self._output_report = self._receive

        self.create_kernel_device()

        now = time.time()
        while not self.uhid_dev_is_ready() and time.time() - now < 5:
            self.dispatch(10)  # pragma: no cover

        self.__logger.debug(f'created endpoint {self.number} ({self.name})')

    def destroy(self):
        for fd in self._opened_files:
            fd.close()
        return super().destroy()

    def udev_input_event(self, device):
        if 'DEVNAME' not in device.properties:
            return

        devname = device.properties['DEVNAME']
        if not devname.startswith('/dev/input/event'):
            return

        # associate the Input type to the matching HID application
        # we reuse the guess work from udev
        types = []
        for name, type in Endpoint.input_type_mapping.items():
            if name in device.properties:
                types.append(type)

        if not types:
            # abort, the device has not been processed by udev
            print('abort', devname, list(device.properties.items()))
            return

        event_node = open(devname, 'rb')
        self._opened_files.append(event_node)
        evdev = libevdev.Device(event_node)

        fd = evdev.fd.fileno()
        flag = fcntl.fcntl(fd, fcntl.F_GETFD)
        fcntl.fcntl(fd, fcntl.F_SETFL, flag | os.O_NONBLOCK)

        for type in types:
            self.input_nodes[type] = evdev

    def udev_event(self, event):
        if event.action != 'add':
            return

        device = event

        subsystem = device.properties['SUBSYSTEM']

        if subsystem == 'input':
            return self.udev_input_event(device)

        self.__logger.debug(f'{subsystem}: {device}')

    def uhid_dev_is_ready(self) -> bool:
        # we consider an endpoint to be ready when we have at least
        # one opened evdev node
        return bool(self.input_nodes)

    def _receive(self, data: List[int], size: int, rtype: int) -> None:
        '''
        Receive data

        Callback called when we receive a HID report.
        Triggers the firmware's callback.

        :param data:    Received data
        :param size:    Received data size
        :param rtype:   Report type
        '''
        data = [struct.unpack('>H', b'\x00' + data[i:i + 1])[0]  # type: ignore
                for i in range(0, size)]

        if size > 0:
            self.logger.debug('read  {}'.format(' '.join(f' {byte:02x}' for byte in data)))

        self._owner.fw.hid_receive(data, size, rtype, self.number)

    def send(self, data: List[int]) -> None:
        '''
        Send data

        Routine used to send a HID report.

        :param data:    Data to send
        '''
        if not data:
            return

        self.__logger.debug('write {}'.format(' '.join(f'{byte:02x}' for byte in data)))

        self.call_input_event(data)

    def create_report(self, action: object, global_data: int = None, skip_empty: bool = True) -> List[int]:
        '''
        Converts action into HID report

        Converts action in HID report according to the report descriptor and
        sends it.

        :param action:      Object holding the desired actions as attributes
        :param global_data: ?
        :param skip_empty:  Enables skipping empty actions
        '''
        empty = True
        for attr in action.__dict__:
            if getattr(action, attr):
                empty = False
                break

        if empty and skip_empty:
            return []

        return super().create_report(action, global_data)
