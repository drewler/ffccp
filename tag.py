import struct
import sys
import re

class Tag:
    offset = 0
    type = ""
    length = 0
    mystery_data = None
    subtags = []
    binary_data = b""
    parsed_data = None
    def __init__(self, stream_data):
        self.offset = stream_data.tell()
        self.type = stream_data.read(4)
        self.length = struct.unpack(">I", stream_data.read(4))[0]
        self.mystery_data = stream_data.read(8)
        self.subtags = []
        binary_data = b""
        parsed_data = None
        while (stream_data.tell() - self.offset) <= self.length:
            first4 = stream_data.read(4)
            if re.match(b"[A-Z| ]{4}", first4):
                stream_data.seek(stream_data.tell() - 4)
                self.subtags.append(Tag(stream_data))
            else:
                self.binary_data.join([first4, stream_data.read(12)])
    def align(self, stream_data, to):
        stream_data.seek(int(stream_data.tell() + to - 1 - (stream_data.tell() - 1) % to))
    def __repr__(self):
        if self.subtags == []:
            return "%s" % self.type
        else:
            return "\n%s - %s" % (self.type, str(self.subtags))    

fh = open(sys.argv[1], "rb");
tagroot = Tag(fh)
print tagroot
