import struct
import sys
import tag

class Skin:
    nodelst = None
    one = None
    def __init__(self, skin_tag):
        self.nodelst = []
        self.one = []
        for skin_subtag in skin_tag.subtags:
            if skin_subtag.type == b"NODE":
                self.parse_node(skin_subtag)
            elif skin_subtag.type == b"ONE ":
                self.parse_one(skin_subtag)
            else:
                print "Unrecognized SKIN subtag : %s" % skin_subtag.type
        print self.nodelst
        for e in self.one:
            print e
    def parse_node(self, node_tag):
        self.nodelst.append(struct.unpack('>2H', node_tag.binary_data[0:node_tag.length]))
    def parse_one(self, one_tag):
        bytes_read = 0
        print one_tag.length
        while bytes_read < one_tag.length:
            #self.one.append(struct.unpack('>7H', one_tag.binary_data[bytes_read:bytes_read+14]))
            len = struct.unpack('>H', one_tag.binary_data[bytes_read:bytes_read+2])[0]
            bytes_read += 2
            print "n: %i" % len
            red = struct.unpack('>%iH' % len, one_tag.binary_data[bytes_read:bytes_read+len*2])
            print red
            bytes_read += len*2