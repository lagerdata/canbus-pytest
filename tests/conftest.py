import pytest
import lager_cantools
import can
from lager import lager

@pytest.fixture(scope='session')
def flash_bootloader(request, fail_bootloader):
    if fail_bootloader:
        pytest.fail('bootloader failed')
        # or the following 2 lines
        # fail_marker = pytest.mark.skip(reason="bootloader failed")
        # request.node.add_marker(fail_marker)

    yield True


@pytest.fixture(scope='session')
def dbc():
    yield lager_cantools.database.load_file('canconv.dbc', strict=False)

@pytest.fixture(scope='session')
def canbus_bitrate():
    yield 500000

@pytest.fixture(scope='session', autouse=True)
def canup(canbus_bitrate):
    lager.can_up([0], canbus_bitrate)
    yield
    lager.can_down([0])

@pytest.fixture(scope='session')
def can0(canbus_type, canbus_bitrate):
    bus = can.interface.Bus(bustype=canbus_type, channel='can0', bitrate=canbus_bitrate, receive_own_messages=True)
    yield bus
    bus.shutdown()

@pytest.fixture(scope='session')
def can1(canbus_type, canbus_bitrate):
    bus = can.interface.Bus(bustype=canbus_type, channel='can1', bitrate=canbus_bitrate, receive_own_messages=True)
    yield bus
    bus.shutdown()

@pytest.fixture(scope='session')
def can2(canbus_type, canbus_bitrate):
    bus = can.interface.Bus(bustype=canbus_type, channel='can2', bitrate=canbus_bitrate, receive_own_messages=True)
    yield bus
    bus.shutdown()

@pytest.fixture(scope='session')
def can3(canbus_type, canbus_bitrate):
    bus = can.interface.Bus(bustype=canbus_type, channel='can3', bitrate=canbus_bitrate, receive_own_messages=True)
    yield bus
    bus.shutdown()
