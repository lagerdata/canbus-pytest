import pytest
import lager_cantools
import can

@pytest.fixture(scope='session')
def flash_bootloader(request, fail_bootloader):
    if fail_bootloader:
        pytest.fail('boatloader failed')
        # or the following 2 lines
        # fail_marker = pytest.mark.skip(reason="bootloader failed")
        # request.node.add_marker(fail_marker)

    yield True


@pytest.fixture(scope='session')
def dbc():
    yield lager_cantools.database.load_file('canconv.dbc', strict=False)


@pytest.fixture(scope='session')
def canbus(canbus_type, canbus_interface):
    yield can.interface.Bus(bustype=canbus_type, channel=canbus_interface, bitrate=500000, receive_own_messages=True)