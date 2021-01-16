import asyncio
import pytest
import can


@pytest.mark.usefixtures("flash_bootloader")
@pytest.mark.incremental
class TestCan:
    @classmethod
    def setup_class(cls):
        pass

    @pytest.mark.asyncio
    async def test_some_asyncio_code(self, can0, event_loop):
        reader = can.AsyncBufferedReader()
        notifier = can.Notifier(can0, [reader], loop=event_loop)
        can0.send(can.Message(arbitration_id=1))
        msg = await reader.get_message()
        assert msg.arbitration_id == 1
        notifier.stop()

    def test_send_receive(self, dbc, can0):
        message = dbc.get_message_by_name('PDU_Info')
        data = message.encode({'Channel': 'A', 'Cycle': 2, 'SlotID': 3, 'UBIT': 1})
        can0.send(can.Message(arbitration_id=message.frame_id, data=data))
        received_message = can0.recv(1)
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
