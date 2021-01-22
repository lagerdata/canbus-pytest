# coding: utf-8

"""
Contains handling of ASC logging files.

"""
import sys
from datetime import datetime
import time
import logging

from can.message import Message
from can.io.generic import BaseIOHandler

CAN_ID_MASK = 0x1FFFFFFF

logger = logging.getLogger('can.io.asc')

class ASCReader(BaseIOHandler):
    """
    Iterator of CAN messages from a ASC logging file. Meta data (comments,
    bus statistics, J1939 Transport Protocol messages) is ignored.

    TODO: turn relative timestamps back to absolute form
    """

    def __init__(self, file):
        """
        :param file: a path-like object or as file-like object to read from
                     If this is a file-like object, is has to opened in text
                     read mode, not binary read mode.
        """
        super(ASCReader, self).__init__(file, mode='r')

    @staticmethod
    def _extract_can_id(str_can_id):
        if str_can_id[-1:].lower() == 'x':
            is_extended = True
            can_id = int(str_can_id[0:-1], 16)
        else:
            is_extended = False
            can_id = int(str_can_id, 16)
        return can_id, is_extended

    def __iter__(self):
        for line in self.file:
            #logger.debug("ASCReader: parsing line: '%s'", line.splitlines()[0])
            temp = line.strip()
            if not temp or not temp[0].isdigit():
                continue
            is_fd = False
            try:
                timestamp, channel, dummy = temp.split(None, 2) # , frameType, dlc, frameData
                if channel == "CANFD":
                    timestamp, _, channel, _, dummy = temp.split(None, 4)
                    is_fd = True

            except ValueError:
                # we parsed an empty comment
                continue

            timestamp = float(timestamp)
            try:
                # See ASCWriter
                channel = int(channel) - 1
            except ValueError:
                pass

            if dummy.strip()[0:10].lower() == 'errorframe':
                msg = Message(timestamp=timestamp, is_error_frame=True,
                              channel=channel)
                yield msg

            elif (not isinstance(channel, int)
                  or dummy.strip()[0:10].lower() == 'statistic:'
                  or dummy.split(None, 1)[0] == "J1939TP"
            ):
                pass

            elif dummy[-1:].lower() == 'r':
                can_id_str, _ = dummy.split(None, 1)
                can_id_num, is_extended_id = self._extract_can_id(can_id_str)
                msg = Message(timestamp=timestamp,
                              arbitration_id=can_id_num & CAN_ID_MASK,
                              is_extended_id=is_extended_id,
                              is_remote_frame=True,
                              channel=channel)
                yield msg

            else:
                brs = None
                esi = None
                data_length = 0
                direction = None
                try:
                    # this only works if dlc > 0 and thus data is available
                    if not is_fd:
                        can_id_str, direction, _, dlc, data = dummy.split(None, 4)
                    else:
                        can_id_str, frame_name, brs, esi, dlc, data_length, data = dummy.split(
                            None, 6
                        )
                        if frame_name.isdigit():
                            # Empty frame_name
                            can_id_str, brs, esi, dlc, data_length, data = dummy.split(
                                None, 5
                            )
                except ValueError:
                    # but if not, we only want to get the stuff up to the dlc
                    can_id_str, direction, _, dlc       = dummy.split(None, 3)
                    # and we set data to an empty sequence manually
                    data = ''
                dlc = int(dlc, 16)
                if is_fd:
                    # For fd frames, dlc and data length might not be equal and
                    # data_length is the actual size of the data
                    dlc = int(data_length)
                frame = bytearray()
                data = data.split()
                for byte in data[0:dlc]:
                    frame.append(int(byte, 16))

                can_id_num, is_extended_id = self._extract_can_id(can_id_str)

                yield direction, Message(
                    timestamp=timestamp,
                    arbitration_id=can_id_num & CAN_ID_MASK,
                    is_extended_id=is_extended_id,
                    is_remote_frame=False,
                    dlc=dlc,
                    data=frame,
                    is_fd=is_fd,
                    channel=channel,
                    bitrate_switch=is_fd and brs == "1",
                    error_state_indicator=is_fd and esi == "1",
                )

        self.stop()


def main(file):
    reader = ASCReader(file)
    for (direction, msg) in reader:
        print(direction, msg)

if __name__ == '__main__':
    main(sys.argv[1])
