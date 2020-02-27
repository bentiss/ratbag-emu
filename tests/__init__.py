# SPDX-License-Identifier: MIT

import os
import sys
f = os.readlink(__file__) if os.path.islink(__file__) else __file__
path = os.path.realpath(os.path.join(f, "..", "..", "src"))

if path not in sys.path:
    sys.path.insert(0, path)

import libevdev  # noqa: 402
import ratbag_emu  # noqa: 402

import pytest  # noqa: 402
import shutil  # noqa: 402
import subprocess  # noqa: 402

from pathlib import Path  # noqa: 402
from time import sleep  # noqa: 402

from ratbag_emu.util import EventData  # noqa: 402


class TestBase(object):
    def reload_udev_rules(self):
        subprocess.run('udevadm control --reload-rules'.split())

    @pytest.fixture(scope='session', autouse=True)
    def udev_rules(self):
        rules_file = '61-ratbag-emu-ignore-test-devices.rules'
        rules_dir = Path('/run/udev/rules.d')

        rules_src = Path('rules.d') / rules_file
        rules_dest = rules_dir / rules_file

        rules_dir.mkdir(exist_ok=True)
        shutil.copyfile(rules_src, rules_dest)
        self.reload_udev_rules()

        yield

        if rules_dest.is_file():
            rules_dest.unlink()
            self.reload_udev_rules()

    def catch_evdev_events(self, device, wait=1):
        sleep(wait)

        received = EventData()
        for e in device.pop_evdev_events():
            if e.matches(libevdev.EV_REL.REL_X):
                received.x += e.value
            elif e.matches(libevdev.EV_REL.REL_Y):
                received.y += e.value

        return received

    def simulate(self, device, action):
        device.simulate_action(action)

        return self.catch_evdev_events(device, wait=action['duration']/1000 + 0.5)
