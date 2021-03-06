import struct
import sys
import re

class Tag:
    offset = None
    type = None
    length = None
    mystery_data = None
    subtags = None
    binary_data = None
    parsed_data = None
    valid_tags = [b"ATRB", b"BANK", b"BINF", b"BUMP", b"CHD ", b"CHM ", b"COLR", b"DGRP", b"DLHD",
                  b"DLST", b"DYN ", b"FMT ", b"FUR ", b"IMAG", b"INFO", b"KEY ", b"MATL", b"MESH",
                  b"MIDX", b"MNAM", b"MSET", b"MSST", b"NAME", b"NODE", b"NORM", b"NSET", b"ONE ",
                  b"PARM", b"QUAN", b"SCEN", b"SEQ ", b"SIZE", b"SKIN", b"TANM", b"TAST", b"TEX ",
                  b"TFRM", b"TIDX", b"TSET", b"TXTR", b"UV  ", b"VERT", b"NAM2", b"DATA", b"ANIM",
                  b"FRAM"]
    def __init__(self, stream_data):
        self.offset = stream_data.tell()
        self.type = stream_data.read(4)
        self.length = struct.unpack(">I", stream_data.read(4))[0]
        self.mystery_data = stream_data.read(8)
        self.subtags = []
        self.binary_data = b""
        self.parsed_data = None
        while (stream_data.tell() - (self.offset + 16)) < self.length:
            first4 = stream_data.read(4)
            stream_data.seek(stream_data.tell() - 4)
            if first4 in self.valid_tags:
                self.subtags.append(Tag(stream_data))
            else:
                readlen = min(16, (self.offset + 16 + self.length) - stream_data.tell())
                self.binary_data = b"".join([self.binary_data, stream_data.read(readlen)])
        self.align(stream_data, 16)
    def align(self, stream_data, to):
        stream_data.seek(int(stream_data.tell() + to - 1 - (stream_data.tell() - 1) % to))
    def __repr__(self):
        if self.subtags == []:
            return "%s" % self.type
        else:
            return "\n%s - %s" % (self.type, str(self.subtags))    

# If called as script, read tags & print them
if __name__ == "__main__":
    fh = open(sys.argv[1], "rb")
    tagroot = Tag(fh)
    print(tagroot)