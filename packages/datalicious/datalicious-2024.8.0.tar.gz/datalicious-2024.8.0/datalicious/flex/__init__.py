"""
FLEX tag information parsers and helpers
"""

import gzip
import struct

from . import tags


class ServiceHeader:
    FORMAT = "c6s11s3sc2s4s12sc"
    SIZE = struct.calcsize(FORMAT)

    def __init__(self, message_length, issue_code):
        self.message_length = message_length
        self.issue_code = issue_code

    @classmethod
    def read(cls, stream):
        header = stream.read(ServiceHeader.SIZE)
        if len(header) == 0:
            return None
        (
            _,
            message_length,
            message_serial_number,
            message_type,
            exchange_code,
            session_distinction,
            issue_classification,
            issue_code,
            _,
        ) = struct.unpack(ServiceHeader.FORMAT, header)
        return cls(int(message_length), int(issue_code))


TAGID_TO_OBJECT = {
    b"NO": tags.NO.from_tag,
    b"ST": tags.ST.from_tag,
    b"VA": tags.VA.from_tag,
    b"VL": tags.VL.from_tag,
    b"1P": tags.PR.from_tag,
    b"QB": tags.QB.from_tag,
    b"QS": tags.QS.from_tag,
    b"SC": tags.SC.from_tag,
    b"BC": tags.BC.from_tag,
}


class UserData:
    def __init__(self, tags, ids=TAGID_TO_OBJECT.keys()):
        self.tags = tags
        self._ids = ids

    @classmethod
    def read(cls, stream, length, ids=TAGID_TO_OBJECT.keys()):
        return cls(
            stream.read(length - ServiceHeader.SIZE)[:-1].split(b"\x13"), ids=ids
        )

    def __repr__(self):
        return f"UserData(tags={[tag[:2].decode() for tag in self.tags]})"

    def __iter__(self):
        for tag_information in self.tags:
            if tag_information[:2] in self._ids:
                yield TAGID_TO_OBJECT[tag_information[:2]](tag_information)

    def __getitem__(self, index):
        tag_information = self.tags[index]
        return TAGID_TO_OBJECT[tag_information[:2]](tag_information)


def read(filename):
    with gzip.open(filename) as stream:
        while True:
            service_header = ServiceHeader.read(stream)
            if service_header is None:
                break
            yield service_header, UserData.read(stream, service_header.message_length)
