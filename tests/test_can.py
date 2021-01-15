import pytest
import can

@pytest.mark.usefixtures("flash_bootloader")
@pytest.mark.incremental
class TestCan:
    @classmethod
    def setup_class(cls):
        pass

    def test_send_receive(self, dbc, canbus):
        message = dbc.get_message_by_name('PDU_Info')
        data = message.encode({'Channel': 'A', 'Cycle': 2, 'SlotID': 3, 'UBIT': 1})
        canbus.send(can.Message(arbitration_id=message.frame_id, data=data))
        received_message = canbus.recv(1)
        assert received_message is not None
        parsed = dbc.decode_message(received_message.arbitration_id, received_message.data)
        assert parsed['Channel'] == 'A'
        assert parsed['Cycle'] == 2
        assert parsed['SlotID'] == 3
        assert parsed['UBIT'] == 1

    def test_bar(self):
        assert 2 == 3

    def test_baz(self):
        assert 3 == 3
